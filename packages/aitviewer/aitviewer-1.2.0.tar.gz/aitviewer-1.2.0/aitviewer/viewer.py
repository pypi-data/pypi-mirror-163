"""
Copyright (C) 2022  ETH Zurich, Manuel Kaufmann, Velko Vechev

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import copy
import os
import moderngl
import moderngl_window
import imgui
import shutil
import tempfile
import numpy as np
import struct

from array import array
from aitviewer.configuration import CONFIG as C
from aitviewer.scene.camera import PinholeCamera
from aitviewer.scene.scene import Scene
from aitviewer.streamables.streamable import Streamable
from aitviewer.utils import images_to_video, PerfTimer
from collections import namedtuple
from moderngl_window import activate_context
from moderngl_window import geometry
from moderngl_window import get_local_window_cls
from moderngl_window.integrations.imgui import ModernglWindowRenderer
from moderngl_window.opengl.vao import VAO
from pathlib import Path
from PIL import Image
from tqdm import tqdm



MeshMouseIntersection = namedtuple('MeshMouseIntersection', 'node tri_id vert_id point_world point_local bc_coords')


class Viewer(moderngl_window.WindowConfig):
    resource_dir = Path(__file__).parent / 'shaders'
    window_type = 'pyqt5'
    size_mult = 1.0
    samples = 4

    def __init__(self, title="AITViewer", size=None, **kwargs):
        """
        Initializer.
        :param title: Window title
        :param size: Window size as (width, height) tuple, if None uses the size from the configuration file
        :param kwargs: kwargs.
        """

        # Window Setup (Following `moderngl_window.run_window_config`).
        base_window_cls = get_local_window_cls(self.window_type)

        # If no size is provided use the size from the configuration file
        if size is None:
            size = C.window_width, C.window_height

        # Calculate window size
        size = int(size[0] * self.size_mult), int(size[1] * self.size_mult)

        self.window = base_window_cls(
            title=title,
            size=size,
            fullscreen=C.fullscreen,
            resizable=C.resizable,
            gl_version=(3, 3),
            aspect_ratio=None,  # Have to set this to None otherwise the window will enforce this aspect ratio.
            vsync=C.vsync,  # Set to False for some performance gains.
            samples=self.samples,
            cursor=True,
        )

        self.window_size = size
        self.window.print_context_info()
        activate_context(window=self.window)

        self.timer = PerfTimer()
        self.ctx = self.window.ctx
        super().__init__(self.ctx, self.window, self.timer)

        # Create GUI context
        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)
        self.imgui_user_interacting = False

        # Setup scene
        self.scene = Scene()
        self.scene.camera = PinholeCamera(45.0)

        # Shaders for rendering the shadow map
        self.raw_depth_prog = self.load_program('shadow_mapping/raw_depth.glsl')
        self.depth_only_prog = self.load_program('shadow_mapping/depth_only.glsl')

        # Mesh mouse intersection
        self.offscreen_p_depth = self.ctx.depth_texture(self.wnd.buffer_size)
        self.offscreen_p_viewpos = self.ctx.texture(self.wnd.buffer_size, 4, dtype='f4')
        self.offscreen_p_tri_id = self.ctx.texture(self.wnd.buffer_size, 4, dtype='f4')
        self.offscreen_p = self.ctx.framebuffer(
            color_attachments=[
                self.offscreen_p_viewpos,
                self.offscreen_p_tri_id
            ],
            depth_attachment=self.offscreen_p_depth
        )
        # Shaders for mesh mouse intersection
        self.frag_map_prog = self.load_program('fragment_picking/frag_map.glsl')
        self.frag_pick_prog = self.load_program('fragment_picking/frag_pick.glsl')
        self.frag_pick_prog['position_texture'].value = 0  # Read from texture channel 0
        self.frag_pick_prog['obj_info_texture'].value = 1  # Read from texture channel 0
        self.picker_output = self.ctx.buffer(reserve=5*4)  # 3 floats, 2 ints
        self.picker_vao = VAO(mode=moderngl.POINTS)

        # For debugging
        self.offscreen_quad = geometry.quad_2d(size=(0.5, 0.5), pos=(0.75, 0.75))

        # Custom UI Font
        self.font_dir = Path(__file__).parent / 'resources' / 'fonts'
        self.fonts = imgui.get_io().fonts
        self.custom_font = self.fonts.add_font_from_file_ttf(os.path.join(self.font_dir, 'Custom.ttf'), 15)
        self.scene.custom_font = self.custom_font
        self.imgui.refresh_font_texture()

        self.modes = {
            'view': {'title': ' View', 'shortcut': 'V'},
            'inspect': {'title': ' Inspect', 'shortcut': 'I'},
        }
        self.selected_mode = 'view'

        self.gui_controls = {
            'menu': self.gui_menu,
            'scene': self.gui_scene,
            'playback': self.gui_playback,
            'inspect': self.gui_inspect,
            'exit': self.gui_exit,
        }

        # Settings
        self.run_animations = C.run_animations
        self.dark_mode = C.dark_mode
        self.playback_fps = C.playback_fps
        self.shadows_enabled = C.shadows_enabled
        self.show_shadow_map = C.show_shadow_map
        self.auto_set_floor = C.auto_set_floor
        self.auto_set_camera_target = C.auto_set_camera_target
        self.backface_culling = C.backface_culling

        self.show_camera_target = False

        self._pan_camera = False
        self._rotate_camera = False
        self._using_temp_camera = False
        self._past_frametimes = np.zeros([60]) - 1.0
        self._last_frame_rendered_at = 0

        self.mmi = None  # Mesh mouse intersection result
        self.animation_range = [0, -1]
        self.video_as_gif = False
        self.video_rotate = False

        # Key Shortcuts
        self._exit_key = self.wnd.keys.ESCAPE
        self._pause_key = self.wnd.keys.SPACE
        self._next_frame_key = self.wnd.keys.PERIOD
        self._previous_frame_key = self.wnd.keys.COMMA
        self._shadow_key = self.wnd.keys.S
        self._orthographic_camera_key = self.wnd.keys.O
        self._mode_inspect = self.wnd.keys.I
        self._mode_view = self.wnd.keys.V
        self._dark_mode_key = self.wnd.keys.D
        self._screenshot_key = self.wnd.keys.P
        self._right_mouse_button = 2  # right
        self._left_mouse_button = 1  # left
        self._save_cam_key = self.wnd.keys.C
        self._load_cam_key = self.wnd.keys.L
        self._show_camera_target_key = self.wnd.keys.T
        self._shortcut_names = {self.wnd.keys.SPACE: "Space",
                                self.wnd.keys.C: "C",
                                self.wnd.keys.D: "D",
                                self.wnd.keys.I: "I",
                                self.wnd.keys.L: "L",
                                self.wnd.keys.O: "O",
                                self.wnd.keys.P: "P",
                                self.wnd.keys.S: "S",
                                self.wnd.keys.T: "T"}

        # Disable exit on escape key
        self.window.exit_key = None
        self._exit_popup_open = False

    def run(self, *args, log=True):
        """
        Enter a blocking visualization loop. This is built following `moderngl_window.run_window_config`.
        :param args: The arguments passed to `config_cls` constructor.
        :param log: Whether to log to the console.
        """
        self.scene.make_renderable(self.ctx)
        if self.auto_set_floor:
            self.scene.auto_set_floor()
            self.scene.backface_culling = self.backface_culling
        if self.auto_set_camera_target:
            self.scene.auto_set_camera_target()
        self.scene.set_lights(self.dark_mode)

        self.animation_range[-1] = self.scene.n_frames - 1

        self.timer.start()
        self._last_frame_rendered_at = self.timer.time

        while not self.window.is_closing:
            current_time, delta = self.timer.next_frame()

            self.window.clear()
            self.window.render(current_time, delta)
            self.window.swap_buffers()
        _, duration = self.timer.stop()
        self.on_close()
        self.window.destroy()
        if duration > 0 and log:
            print("Duration: {0:.2f}s @ {1:.2f} FPS".format(duration, self.window.frames / duration))

    def render(self, time, frame_time):
        """The main drawing function."""

        # Advance up to 100 frames to avoid looping for too long if the playback speed is too high
        for _ in range(100):
            # Check if we need to advance the sequences. 
            if self.run_animations and time - self._last_frame_rendered_at > 1.0 / self.playback_fps:
                self.scene.next_frame()
                self._last_frame_rendered_at += 1.0 / self.playback_fps
            else:
                break
        
        
        #Update camera matrices that will be used for rendering
        self.scene.camera.update_matrices(self.window.size[0], self.window.size[1])

        self.streamable_capture()
        self.render_fragmap()
        self.render_shadowmap()
        self.render_prepare()
        self.render_scene()

        if self.show_shadow_map:
            self.offscreen_p_depth.use(location=0)
            self.offscreen_quad.render(self.frag_map_prog)

        # FPS accounting.
        self._past_frametimes[:-1] = self._past_frametimes[1:]
        self._past_frametimes[-1] = frame_time

        # Render the UI components.
        self.gui()

    def streamable_capture(self):
        # Collect all streamable nodes
        rs = self.scene.collect_nodes(obj_type=Streamable)
        for r in rs:
            r.capture()

    def render_shadowmap(self):
        """A pass to render the shadow map, i.e. render the entire scene once from the view of the light."""
        self.ctx.enable_only(moderngl.DEPTH_TEST)
        if self.shadows_enabled:
            rs = self.scene.collect_nodes()
            
            for light in self.scene.lights:
                if light.shadow_enabled:
                    light.use(self.ctx)
                    light_matrix = light.mvp()
                    for r in rs:
                        r.render_shadowmap(light_matrix, self.depth_only_prog)

    def render_fragmap(self):
        """A pass to render the fragment picking map, i.e. render the scene with world coords as colors."""
        self.ctx.enable_only(moderngl.DEPTH_TEST)
        self.offscreen_p.clear()
        self.offscreen_p.use()
        rs = self.scene.collect_nodes()
        for r in rs:
            r.render_fragmap(self.scene.camera, self.frag_map_prog, self.wnd.buffer_size)

    def render_scene(self):
        """Render the current scene to the framebuffer without time accounting and GUI elements."""
        self.scene.render(window_size=self.window.size,
                          lights=self.scene.lights,
                          shadows_enabled=self.shadows_enabled,
                          show_camera_target=self.show_camera_target and not self._using_temp_camera,
                          depth_prepass_prog=self.depth_only_prog)

    def render_prepare(self):
        """Prepare the framebuffer."""
        self.wnd.use()
        # Clear background and make sure only the flags we want are enabled.
        if self.dark_mode:
            self.ctx.clear(0.1, 0.1, 0.1, 1.0)
        else:
            self.ctx.clear(1.0, 1.0, 1.0, 1.0)

        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.BLEND | moderngl.CULL_FACE)
        self.ctx.cull_face = 'back'
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA

    def prevent_background_interactions(self):
        """Prevent background interactions when hovering over any imgui window."""
        self.imgui_user_interacting = self.imgui.io.want_capture_mouse

    def toggle_animation(self, run: bool):
        self.run_animations = run
        if self.run_animations:
            self._last_frame_rendered_at = self.timer.time

    def reset_camera(self):
        if self._using_temp_camera:
            self._using_temp_camera = False

            fwd = self.scene.camera.forward
            pos = self.scene.camera.position

            self.scene.camera = PinholeCamera(45)
            self.scene.camera.position = np.copy(pos)
            self.scene.camera.target = pos + fwd * 3
            self.scene.camera.update_matrices(self.window_size[0], self.window_size[1])
            
    def set_temp_camera(self, camera):
        self.scene.camera = camera
        self._using_temp_camera = True

    def gui(self):
        imgui.new_frame()

        # Reset user interacting state
        self.imgui_user_interacting = False

        # Render user controls
        for gc in self.gui_controls.values(): gc()

        # Contains live examples of all possible displays/controls - useful for browsing for new components
        # imgui.show_test_window()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    def gui_scene(self):
        # Render scene GUI
        imgui.begin(self.scene.name, True)
        self.scene.gui(imgui)
        self.prevent_background_interactions()
        imgui.end()

    def gui_menu(self):
        clicked_export = False

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True)
                if clicked_quit:
                    exit(1)

                clicked_export, selected_export = imgui.menu_item(
                    "Save as video..", None, False, True)

                clicked_export360, _ = imgui.menu_item(
                    "Save as 360 video..", None, False, enabled=isinstance(self.scene.camera, PinholeCamera))
                if clicked_export360:
                    self.to_360_deg_video()

                clicked_screenshot, selected_screenshot = imgui.menu_item(
                    "Screenshot", self._shortcut_names[self._screenshot_key], False, True)
                if clicked_screenshot:
                    self.take_screenshot()

                imgui.end_menu()

            if imgui.begin_menu("View", True):
                _, self.shadows_enabled = imgui.menu_item("Render Shadows", self._shortcut_names[self._shadow_key],
                                                          self.shadows_enabled, True)
                # _, self.show_shadow_map = imgui.menu_item("Show Shadow Map", None, self.show_shadow_map, True)
                _, self.dark_mode = imgui.menu_item("Dark Mode", self._shortcut_names[self._dark_mode_key],
                                                    self.dark_mode, True)
                _, self.show_camera_target = imgui.menu_item("Show Camera Target", self._shortcut_names[self._show_camera_target_key],
                                                    self.show_camera_target, True)

                is_ortho = False if self._using_temp_camera else self.scene.camera.is_ortho
                _, is_ortho = imgui.menu_item("Orthographic Camera",
                                                                self._shortcut_names[self._orthographic_camera_key],
                                                is_ortho, True)
                if is_ortho and self._using_temp_camera:
                    self.reset_camera()
                self.scene.camera.is_ortho = is_ortho

                clicked_save_cam, selected_save_cam = imgui.menu_item("Save Camera",
                                                                self._shortcut_names[self._save_cam_key],
                                                                False, True)
                if clicked_save_cam:
                    self.reset_camera()
                    self.scene.camera.save_cam()

                clicked_load_cam, selected_load_cam = imgui.menu_item("Load Camera",
                                                                self._shortcut_names[self._load_cam_key],
                                                                False, True)

                if clicked_load_cam:
                    self.reset_camera()
                    self.scene.camera.load_cam()

                imgui.end_menu()

            if imgui.begin_menu("Mode", True):
                for id, mode in self.modes.items():
                    mode_clicked, _ = imgui.menu_item(mode['title'], mode['shortcut'], id == self.selected_mode, True)
                    if mode_clicked:
                        self.selected_mode = id

                imgui.end_menu()
            imgui.end_main_menu_bar()

        if clicked_export:
            imgui.open_popup("Export Video")
        if imgui.begin_popup_modal("Export Video", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)[0]:
            imgui.text("Enter Range for Video Export.")
            rcu, animation_range = imgui.drag_int2('Range##range_control', *self.animation_range,
                                                   min_value=0,  max_value=self.scene.n_frames-1)
            if rcu:
                self.animation_range[0] = max(animation_range[0], 0)
                self.animation_range[1] = min(animation_range[-1], self.scene.n_frames-1)
            _, self.video_as_gif = imgui.checkbox("GIF instead of MP4", self.video_as_gif)
            
            if isinstance(self.scene.camera, PinholeCamera):
                _, self.video_rotate = imgui.checkbox("Animate and rotate", self.video_rotate)
            else:
                imgui.push_style_var(imgui.STYLE_ALPHA, 0.2)
                imgui.checkbox("Animate and rotate", False)
                imgui.pop_style_var(1)

            
            imgui.spacing()

            # Draw a cancel and exit button on the same line using the available space
            button_width = (imgui.get_content_region_available()[0] - imgui.get_style().item_spacing[0]) * 0.5
            
            # Style the cancel with a grey color
            imgui.push_style_color(imgui.COLOR_BUTTON, 0.5, 0.5, 0.5, 1.0)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE,  0.6, 0.6, 0.6, 1.0)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.7, 0.7, 0.7, 1.0)

            if imgui.button("cancel", width=button_width):
                imgui.close_current_popup()

            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()

            imgui.same_line()
            if imgui.button("export", button_width):
                imgui.close_current_popup()
                self.to_video(self.video_rotate)

            self.prevent_background_interactions()
            imgui.end_popup()

    def gui_playback(self):
        """GUI to control playback settings."""
        imgui.begin("Playback", True)
        u, run_animations = imgui.checkbox("Run animations [{}]".format(self._shortcut_names[self._pause_key]),
                                                self.run_animations)
        if u:
            self.toggle_animation(run_animations)

        # Plot FPS
        frametime_avg = np.mean(self._past_frametimes[self._past_frametimes > 0.0])
        fps_avg = 1 / frametime_avg
        ms_avg = frametime_avg * 1000.0 
        
        imgui.plot_lines("Internal {:.1f} fps @ {:.2f} ms/frame".format(fps_avg, ms_avg),
                         array('f', (1.0 / self._past_frametimes).tolist()),
                         scale_min=0, scale_max=100.0, graph_size=(100, 20))

        _, self.playback_fps = imgui.drag_float('Target Playback fps##playback_fps', self.playback_fps, 0.1,
                                                min_value=1.0, max_value=120.0, format='%.1f')

        # Sequence Control
        # For simplicity, we allow the global sequence slider to only go as far as the shortest known sequence.
        n_frames = self.scene.n_frames

        _, self.scene.current_frame_id = imgui.slider_int('Frame##r_global_seq_control', self.scene.current_frame_id,
                                                          min_value=0, max_value=n_frames - 1)
        self.prevent_background_interactions()
        imgui.end()

    def gui_inspect(self):
        """GUI to control playback settings."""
        if self.selected_mode == 'inspect':
            imgui.begin("Inspect", True)

            if self.mmi is not None:
                for k, v in zip(self.mmi._fields, self.mmi):
                    imgui.text("{}: {}".format(k, v))

            self.prevent_background_interactions()
            imgui.end()

    def gui_exit(self):
        if self._exit_popup_open:    
            imgui.open_popup("Exit##exit-popup")

        if imgui.begin_popup_modal("Exit##exit-popup", flags=imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)[0]:
            if self._exit_popup_open:    
                imgui.text("Are you sure you want to exit?")
                imgui.spacing()

                # Draw a cancel and exit button on the same line using the available space
                button_width = (imgui.get_content_region_available()[0] - imgui.get_style().item_spacing[0]) * 0.5
                
                # Style the cancel with a grey color
                imgui.push_style_color(imgui.COLOR_BUTTON, 0.5, 0.5, 0.5, 1.0)
                imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE,  0.6, 0.6, 0.6, 1.0)
                imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.7, 0.7, 0.7, 1.0)

                if imgui.button("cancel", width=button_width):
                    imgui.close_current_popup()
                    self._exit_popup_open = False

                imgui.pop_style_color()
                imgui.pop_style_color()
                imgui.pop_style_color()

                imgui.same_line()
                if imgui.button("exit", button_width):
                    self.window.close()
            else:
                imgui.close_current_popup()
            imgui.end_popup()

    def mesh_mouse_intersection(self, x: int, y: int):
        """Given an x/y screen coordinate, get the intersected object, triangle id, and xyz point in camera space"""

        # Texture is y=0 at bottom, so we flip y coords
        pos = int(x * self.wnd.pixel_ratio), int(self.wnd.buffer_height - (y * self.wnd.pixel_ratio))

        # Fragment picker uses already encoded position/object/triangle in the frag_pos program textures
        self.frag_pick_prog['texel_pos'].value = pos
        self.offscreen_p_viewpos.use(location=0)
        self.offscreen_p_tri_id.use(location=1)
        self.picker_vao.transform(self.frag_pick_prog, self.picker_output, vertices=1)
        x, y, z, obj_id, tri_id = struct.unpack('3f2i', self.picker_output.read())

        if obj_id > 0 and tri_id > 0:
            node = self.scene.get_node_by_uid(obj_id)
            # Camera space to world space
            point_world = np.array(np.linalg.inv(self.scene.camera.get_view_matrix()) @ np.array((x, y, z, 1.0)))[:-1]
            point_local = (np.linalg.inv(node.model_matrix()) @ np.append(point_world, 1.0))[:-1]
            vert_id = node.closest_vertex_in_triangle(tri_id, point_local)
            bc_coords = node.get_bc_coords_from_points(tri_id, [point_local])
            return MeshMouseIntersection(node, tri_id, vert_id, point_world, point_local, bc_coords)

        return None

    def resize(self, width: int, height: int):
        self.window_size = (width, height)
        self.imgui.resize(width, height)

    def key_event(self, key, action, modifiers):
        self.imgui.key_event(key, action, modifiers)

        # Handle keyboard shortcuts when the exit modal is open
        if action == self.wnd.keys.ACTION_PRESS and self._exit_popup_open:
            if key == self.wnd.keys.ENTER:
                self.window.close()
            elif key == self._exit_key:
                self._exit_popup_open = False
            return

        if self.imgui.io.want_capture_keyboard:
            return

        if action == self.wnd.keys.ACTION_PRESS:
            if key == self._exit_key:
                self._exit_popup_open = True

            if key == self._pause_key:
                self.toggle_animation(not self.run_animations)

            elif key == self._next_frame_key:
                if not self.run_animations:
                    self.scene.next_frame()

            elif key == self._previous_frame_key:
                if not self.run_animations:
                    self.scene.previous_frame()

            elif key == self._shadow_key:
                self.shadows_enabled = not self.shadows_enabled

            elif key == self._show_camera_target_key:
                self.show_camera_target = not self.show_camera_target

            elif key == self._orthographic_camera_key:
                if self._using_temp_camera:
                    self.reset_camera()
                self.scene.camera.is_ortho = not self.scene.camera.is_ortho

            elif key == self._mode_view:
                self.selected_mode = 'view'

            elif key == self._mode_inspect:
                self.selected_mode = 'inspect'

            elif key == self._dark_mode_key:
                self.dark_mode = not self.dark_mode
                self.scene.set_lights(self.dark_mode)

            elif key == self._screenshot_key:
                self.take_screenshot()
            elif key == self._save_cam_key:
                if self._using_temp_camera:
                    self.reset_camera()
                self.scene.camera.save_cam()
            elif key == self._load_cam_key:
                if self._using_temp_camera:
                    self.reset_camera()
                self.scene.camera.load_cam()

        if action == self.wnd.keys.ACTION_RELEASE:
            pass

    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

        if self.selected_mode == 'inspect':
            self.mmi = self.mesh_mouse_intersection(x, y)

    def mouse_press_event(self, x: int, y: int, button: int):
        self.imgui.mouse_press_event(x, y, button)

        if not self.imgui_user_interacting:
            self._pan_camera = button == self._right_mouse_button
            self._rotate_camera = button == self._left_mouse_button

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

        if button == self._right_mouse_button:
            self._pan_camera = False
        if button == self._left_mouse_button:
            self._rotate_camera = False

    def mouse_drag_event(self, x: int, y: int, dx: int, dy: int):
        self.imgui.mouse_drag_event(x, y, dx, dy)

        if not self.imgui_user_interacting :
            if self._pan_camera:
                if self._using_temp_camera:
                    self.reset_camera()
                self.scene.camera.pan(dx, dy)

            if self._rotate_camera:
                if self._using_temp_camera:
                    self.reset_camera()
                self.scene.camera.rotate_azimuth_elevation(dx, dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

        if not self.imgui_user_interacting:
            if self._using_temp_camera:
                self.reset_camera()
            self.scene.camera.dolly_zoom(np.sign(y_offset), self.wnd.modifiers.shift)

    def unicode_char_entered(self, char):
        self.imgui.unicode_char_entered(char)

    def save_current_frame_as_image(self, frame_dir, frame_id):
        """Saves the current frame as an image to disk."""
        image = self.get_current_frame_as_image()
        image_name = os.path.join(frame_dir, 'frame_{:0>6}.png'.format(frame_id))
        image.save(image_name)

    def get_current_frame_as_image(self):
        """Return the FBO content as a PIL image."""
        image = Image.frombytes('RGB',
                                (self.wnd.fbo.viewport[2] - self.wnd.fbo.viewport[0],
                                 self.wnd.fbo.viewport[3] - self.wnd.fbo.viewport[1]),
                                self.wnd.fbo.read(viewport=self.wnd.fbo.viewport, alignment=1))
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image

    def on_close(self):
        """
        Clean up before destroying the window
        """
        # Shut down all streams
        for s in self.scene.collect_nodes(obj_type=Streamable):
            s.stop()

    def take_screenshot(self):
        """Save the current framebuffer to an image."""
        frame_dir = C.export_dir + '/screenshots/'
        if not os.path.exists(frame_dir):
            os.makedirs(frame_dir)
        # We don't want to export GUI elements, so render the scene again.
        self.render_shadowmap()
        self.render_prepare()
        self.render_scene()
        self.save_current_frame_as_image(frame_dir, self.scene.current_frame_id)

    def to_video(self, rotate=False):
        """Render the loaded animations to video."""

        if self.animation_range[-1] < self.animation_range[0]:
            print("No frames rendered.")
            return

        if rotate and not isinstance(self.scene.camera, PinholeCamera):
            print("Cannot export an animated video while using a camera that is not a PinholeCamera")
            return 

        # Start all sequences from 0 but remember where we left off.
        saved_curr_frame = self.scene.current_frame_id

        # Create a temporary directory to render frames to.
        frame_dir = tempfile.TemporaryDirectory().name
        os.makedirs(frame_dir)

        # Store the current camera and create a copy of if required
        saved_camera = self.scene.camera
        if rotate:
            self.scene.camera = copy.deepcopy(self.scene.camera)

        az_delta = 2 * np.pi / (self.animation_range[-1]+1)

        # Render each frame to an image file.
        print("Saving frames to {}".format(frame_dir))
        progress_bar = tqdm(total=self.animation_range[-1]-self.animation_range[0], desc='Rendering frames')

        for i, f in enumerate(range(self.animation_range[0], self.animation_range[-1]+1)):
            if rotate:
                self.scene.camera.rotate_azimuth(az_delta)

            self.scene.current_frame_id = f
            self.scene.camera.update_matrices(self.window.size[0], self.window.size[1])
            self.render_shadowmap()
            self.render_prepare()
            self.render_scene()
            self.save_current_frame_as_image(frame_dir, i)
            progress_bar.update()
        progress_bar.close()

        # Export to video.
        suffix = '.gif' if self.video_as_gif else '.mp4'
        images_to_video(frame_dir, C.export_dir + '/videos/' + self.window.title + suffix, input_fps=self.playback_fps,
                        output_fps=60)

        # Remove temp frames.
        shutil.rmtree(frame_dir)

        # Reset frame IDs.
        self.scene.current_frame_id = saved_curr_frame
        self.scene.camera = saved_camera

        print("Done.")

    def to_360_deg_video(self):
        """Matrix shot. Keeps the look-at point fixed and rotates the camera around it."""
        if not isinstance(self.scene.camera, PinholeCamera):
            print("Cannot export a 360 video while using a camera that is not a PinholeCamera")
            return

        n_frames = 360
        saved_camera = copy.deepcopy(self.scene.camera)

        angles = -np.arange(0, 2*np.pi, 2*np.pi/n_frames)
        cam_centered = self.scene.camera.position - self.scene.camera.target
        new_x = cam_centered[0] * np.cos(angles) - cam_centered[2] * np.sin(angles) + self.scene.camera.target[0]
        new_z = cam_centered[0] * np.sin(angles) + cam_centered[2] * np.cos(angles) + self.scene.camera.target[2]
        circle = np.stack([new_x, np.zeros_like(new_x) + self.scene.camera.position[1], new_z]).T

        # Create a temporary directory to render frames to.
        frame_dir = tempfile.TemporaryDirectory().name
        os.makedirs(frame_dir)

        # Render each frame to an image file.
        print("Saving frames to {}".format(frame_dir))
        progress_bar = tqdm(total=n_frames, desc='Rendering frames')
        for f in range(circle.shape[0]):
            self.scene.camera.position = circle[f]
            self.scene.camera.update_matrices(self.window.size[0], self.window.size[1])
            self.render_shadowmap()
            self.render_prepare()
            self.render_scene()
            self.save_current_frame_as_image(frame_dir, f)
            progress_bar.update()
        progress_bar.close()

        # Export to video.
        images_to_video(frame_dir, C.export_dir + '/videos/' + self.window.title + '_360deg.mp4')

        # Remove temp frames.
        shutil.rmtree(frame_dir)

        # Reset Camera.
        self.scene.camera = saved_camera

        print("Done.")
