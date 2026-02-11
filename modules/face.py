from vispy import scene, app
import numpy as np
from queue import Queue

class FaceController:
    COLORS = {
        "listening": np.array([0, 0, 1, 1], dtype=np.float32),
        "thinking": np.array([0, 1, 0, 1], dtype=np.float32),
        "error": np.array([1, 0, 0, 1], dtype=np.float32),
        "sleeping": np.array([1, 1, 0, 1], dtype=np.float32),  # yellow
    }

    BASE_SIZE = 3
    BASE_RADIUS = 1.0

    def __init__(self):
        self.state_queue = Queue()
        self.current_color = self.COLORS["listening"].copy()
        self.target_color = self.COLORS["listening"].copy()
        self.n_points = 400
        self.points = self.generate_points(self.n_points)

        # Pulse / breathing
        self.base_radius = self.BASE_RADIUS
        self.current_radius = self.base_radius
        self.target_radius = self.base_radius
        self.pulse_value = 0.0
        self.pulse_dir = 1
        self.z_wobble = 0.0
        self.z_dir = 1
        self.current_state = "listening"

        # SceneCanvas
        self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
                                        show=True, title="Jarvis AI Face")
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
        self.scatter = scene.visuals.Markers(parent=self.view.scene)
        self.scatter.set_data(self.points, face_color=self.current_color, size=self.BASE_SIZE)

        # Precompute slow rotation matrix
        self.angle = 0.002
        c, s = np.cos(self.angle), np.sin(self.angle)
        self.rot_mat = np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])

        # Timer for updates
        self.timer = app.Timer(interval=1/60.0, connect=self.update, start=True)

    def generate_points(self, n):
        theta = np.random.uniform(0, 2*np.pi, n)
        phi = np.random.uniform(0, np.pi, n)
        r = np.random.uniform(0.5, 1.0, n)
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.c_[x, y, z]

    def set_state(self, state: str):
        if state in self.COLORS:
            self.state_queue.put(state)

    def update(self, event):
        # Apply queued state changes smoothly
        while not self.state_queue.empty():
            state = self.state_queue.get()
            self.target_color = self.COLORS[state].copy()
            self.current_state = state

            if state == "listening":
                self.target_radius = self.base_radius
            elif state == "thinking":
                self.target_radius = self.base_radius * 1.1
            elif state == "sleeping":
                self.target_radius = self.base_radius * 0.5  # exactly half-size
            else:  # error or default
                self.target_radius = self.base_radius

            # Reset pulse/wobble
            self.pulse_value = 0.0
            self.pulse_dir = 1
            self.z_wobble = 0.0
            self.z_dir = 1

        # Smooth color transition
        self.current_color += (self.target_color - self.current_color) * 0.05

        # Pulse & wobble per state
        if self.current_state == "thinking":
            pulse_speed = 0.001
            pulse_strength = self.target_radius * 0.03
            z_speed = 0.001
            z_strength = 0.005
        elif self.current_state == "listening":
            pulse_speed = 0.0000005
            pulse_strength = self.target_radius * 0.02
            z_speed = 0.00005
            z_strength = 0.0003
        elif self.current_state == "error":
            pulse_speed = 0.000005
            pulse_strength = self.target_radius * 0.03
            z_speed = 0.005
            z_strength = 0.05
        elif self.current_state == "sleeping":
            pulse_speed = 0.0005  # very slow
            pulse_strength = self.target_radius * 0.05  # tiny pulse relative to half-size
            z_speed = 0.0003  # gentle wobble
            z_strength = 0.002
        else:  # error or default
            pulse_speed = 0
            pulse_strength = 0
            z_speed = 0
            z_strength = 0

        # Update pulse (grow/shrink)
        self.pulse_value += self.pulse_dir * pulse_speed
        if self.pulse_value > pulse_strength or self.pulse_value < -pulse_strength:
            self.pulse_dir *= -1

        # Smooth radius toward target + pulse
        self.current_radius += (self.target_radius + self.pulse_value - self.current_radius) * 0.3

        # Update z-axis wobble
        self.z_wobble += self.z_dir * z_speed
        if self.z_wobble > z_strength or self.z_wobble < -z_strength:
            self.z_dir *= -1

        # Rotate points slowly
        self.points = self.points @ self.rot_mat.T

        # Apply radius and z wobble
        scaled_points = self.points * self.current_radius
        scaled_points[:, 2] += self.z_wobble

        # Update scatter
        self.scatter.set_data(scaled_points, face_color=self.current_color, size=self.BASE_SIZE)

    # def update(self, event):
    #     # Apply queued state changes smoothly
    #     while not self.state_queue.empty():
    #         state = self.state_queue.get()
    #         self.target_color = self.COLORS[state].copy()
    #         self.current_state = state
    #         if state == "listening":
    #             self.target_radius = self.base_radius
    #         elif state == "thinking" or 'error':
    #             self.target_radius = self.base_radius * 1.1
    #         elif state == "sleeping":
    #             self.target_radius = self.base_radius * 0.5
    #             self.pulse_value = 0.0
    #             self.pulse_dir = 1
    #         else:
    #             self.target_radius = self.base_radius
    #         self.pulse_value = 0.0
    #         self.pulse_dir = 1
    #         self.z_wobble = 0.0
    #         self.z_dir = 1
    #
    #     # Smooth color blending
    #     self.current_color += (self.target_color - self.current_color) * 0.05
    #
    #     # Pulse & wobble parameters per state
    #     # Pulse parameters per state
    #     if self.current_state == "thinking":
    #         pulse_speed = 0.001
    #         pulse_strength = 0.01
    #         z_speed = 0.001
    #         z_strength = 0.005
    #     elif self.current_state == "listening":
    #         pulse_speed = 0.0000005
    #         pulse_strength = 0.0000005
    #         z_speed = 0.000005
    #         z_strength = 0.00002
    #     elif self.current_state == "error":
    #         pulse_speed = 0.000005
    #         pulse_strength = 0.00005
    #         z_speed = 0.005
    #         z_strength = 0.05
    #     elif self.current_state == "sleeping":
    #         pulse_speed = 0.00000005   # slowest
    #         pulse_strength = 0.0000005
    #         z_speed = 0.0005
    #         z_strength = 0.005
    #     else:  # error or default
    #         pulse_speed = 0
    #         pulse_strength = 0
    #         z_speed = 0
    #         z_strength = 0
    #         self.current_radius = self.base_radius
    #         self.z_wobble = 0.0
    #
    #     # Update pulse (grow/shrink)
    #     self.pulse_value += self.pulse_dir * pulse_speed
    #     if self.pulse_value > pulse_strength or self.pulse_value < -pulse_strength:
    #         self.pulse_dir *= -1
    #     self.current_radius += (self.target_radius + self.pulse_value - self.current_radius) * 0.1  # smooth radius transition
    #
    #     # Update z-axis wobble
    #     self.z_wobble += self.z_dir * z_speed
    #     if self.z_wobble > z_strength or self.z_wobble < -z_strength:
    #         self.z_dir *= -1
    #
    #     # Rotate points slowly
    #     self.points = self.points @ self.rot_mat.T
    #
    #     # Apply radius and z wobble
    #     scaled_points = self.points * self.current_radius
    #     scaled_points[:, 2] += self.z_wobble
    #
    #     # Update scatter
    #     self.scatter.set_data(scaled_points, face_color=self.current_color, size=self.BASE_SIZE)

    def run(self):
        app.run()













# from vispy import scene, app
# import numpy as np
# from queue import Queue
#
# class FaceController:
#     COLORS = {
#         "listening": np.array([0, 0, 1, 1], dtype=np.float32),
#         "thinking": np.array([0, 1, 0, 1], dtype=np.float32),
#         "error": np.array([1, 0, 0, 1], dtype=np.float32),
#         "sleeping": np.array([1, 1, 0, 1], dtype=np.float32),  # Yellow for sleep
#     }
#
#     BASE_SIZE = 3
#     BASE_RADIUS = 1.0
#
#     def __init__(self):
#         self.state_queue = Queue()
#         self.current_color = self.COLORS["listening"].copy()
#         self.target_color = self.COLORS["listening"].copy()
#         self.n_points = 400
#         self.points = self.generate_points(self.n_points)
#
#         # Pulse / breathing
#         self.base_radius = self.BASE_RADIUS
#         self.current_radius = self.base_radius
#         self.target_radius = self.base_radius
#         self.pulse_value = 0.0
#         self.pulse_dir = 1
#         self.z_wobble = 0.0
#         self.z_dir = 1
#         self.current_state = "listening"
#
#         # SceneCanvas
#         self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
#                                         show=True, title="Jarvis AI Face")
#         self.view = self.canvas.central_widget.add_view()
#         self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
#         self.scatter = scene.visuals.Markers(parent=self.view.scene)
#         self.scatter.set_data(self.points, face_color=self.current_color, size=self.BASE_SIZE)
#
#         # Precompute rotation matrix (very slow)
#         self.angle = 0.002
#         c, s = np.cos(self.angle), np.sin(self.angle)
#         self.rot_mat = np.array([
#             [c, -s, 0],
#             [s,  c, 0],
#             [0,  0, 1]
#         ])
#
#         # Timer for updates
#         self.timer = app.Timer(interval=1/60.0, connect=self.update, start=True)
#
#     def generate_points(self, n):
#         theta = np.random.uniform(0, 2*np.pi, n)
#         phi = np.random.uniform(0, np.pi, n)
#         r = np.random.uniform(0.5, 1.0, n)
#         x = r * np.sin(phi) * np.cos(theta)
#         y = r * np.sin(phi) * np.sin(theta)
#         z = r * np.cos(phi)
#         return np.c_[x, y, z]
#
#     def set_state(self, state: str):
#         if state in self.COLORS:
#             self.state_queue.put(state)
#
#     def update(self, event):
#         # Apply queued state changes
#         while not self.state_queue.empty():
#             state = self.state_queue.get()
#             self.target_color = self.COLORS[state].copy()
#             self.current_state = state
#             if state == "listening":
#                 self.target_radius = self.base_radius
#             elif state == "thinking":
#                 self.target_radius = self.base_radius * 1.1
#             elif state == "sleeping":
#                 self.target_radius = self.base_radius * 0.5  # same radius, but slower effects
#             else:
#                 self.target_radius = self.base_radius
#             self.pulse_value = 0.0
#             self.pulse_dir = 1
#             self.z_wobble = 0.0
#             self.z_dir = 1
#
#         # Smooth color transition
#         self.current_color += (self.target_color - self.current_color) * 0.05
#
#         # Pulse parameters per state
#         if self.current_state == "thinking":
#             pulse_speed = 0.001
#             pulse_strength = 0.01
#             z_speed = 0.001
#             z_strength = 0.005
#         elif self.current_state == "listening":
#             pulse_speed = 0.0000005
#             pulse_strength = 0.0000005
#             z_speed = 0.000005
#             z_strength = 0.00002
#         elif self.current_state == "error":
#             pulse_speed = 0.000005
#             pulse_strength = 0.00005
#             z_speed = 0.005
#             z_strength = 0.05
#         elif self.current_state == "sleeping":
#             pulse_speed = 0.00000005   # slowest
#             pulse_strength = 0.0000005
#             z_speed = 0.0005
#             z_strength = 0.005
#         else:  # error or default
#             pulse_speed = 0
#             pulse_strength = 0
#             z_speed = 0
#             z_strength = 0
#             self.current_radius = self.base_radius
#             self.z_wobble = 0.0
#
#         # Update pulse
#         self.pulse_value += self.pulse_dir * pulse_speed
#         if self.pulse_value > pulse_strength or self.pulse_value < -pulse_strength:
#             self.pulse_dir *= -1
#         self.current_radius = self.target_radius + self.pulse_value
#
#         # Update z-axis wobble
#         self.z_wobble += self.z_dir * z_speed
#         if self.z_wobble > z_strength or self.z_wobble < -z_strength:
#             self.z_dir *= -1
#
#         # Rotate points slowly
#         self.points = self.points @ self.rot_mat.T
#
#         # Apply radius and z wobble
#         scaled_points = self.points * self.current_radius
#         scaled_points[:, 2] += self.z_wobble
#
#         # Update scatter
#         self.scatter.set_data(scaled_points, face_color=self.current_color, size=self.BASE_SIZE)
#
#     def run(self):
#         app.run()







# from vispy import scene, app
# import numpy as np
# from queue import Queue
#
# class FaceController:
#     COLORS = {
#         "listening": np.array([0, 0, 1, 1], dtype=np.float32),
#         "thinking": np.array([0, 1, 0, 1], dtype=np.float32),
#         "error": np.array([1, 0, 0, 1], dtype=np.float32)
#     }
#
#     BASE_SIZE = 3
#     BASE_RADIUS = 1.0
#
#     def __init__(self):
#         self.state_queue = Queue()
#         self.current_color = self.COLORS["listening"].copy()
#         self.target_color = self.COLORS["listening"].copy()
#         self.n_points = 400
#         self.points = self.generate_points(self.n_points)
#
#         # Pulse / breathing
#         self.base_radius = self.BASE_RADIUS
#         self.current_radius = self.base_radius
#         self.target_radius = self.base_radius
#         self.pulse_value = 0.0
#         self.pulse_dir = 1
#         self.z_wobble = 0.0
#         self.z_dir = 1
#         self.current_state = "listening"
#
#         # SceneCanvas
#         self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
#                                         show=True, title="Jarvis AI Face")
#         self.view = self.canvas.central_widget.add_view()
#         self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
#         self.scatter = scene.visuals.Markers(parent=self.view.scene)
#         self.scatter.set_data(self.points, face_color=self.current_color, size=self.BASE_SIZE)
#
#         # Precompute rotation matrix
#         self.angle = 0.01
#         c, s = np.cos(self.angle), np.sin(self.angle)
#         self.rot_mat = np.array([
#             [c, -s, 0],
#             [s,  c, 0],
#             [0,  0, 1]
#         ])
#
#         # Timer for updates
#         self.timer = app.Timer(interval=1/60.0, connect=self.update, start=True)
#
#     def generate_points(self, n):
#         theta = np.random.uniform(0, 2*np.pi, n)
#         phi = np.random.uniform(0, np.pi, n)
#         r = np.random.uniform(0.5, 1.0, n)
#         x = r * np.sin(phi) * np.cos(theta)
#         y = r * np.sin(phi) * np.sin(theta)
#         z = r * np.cos(phi)
#         return np.c_[x, y, z]
#
#     def set_state(self, state: str):
#         if state in self.COLORS:
#             self.state_queue.put(state)
#
#     def update(self, event):
#         # Apply queued state changes
#         while not self.state_queue.empty():
#             state = self.state_queue.get()
#             self.target_color = self.COLORS[state].copy()
#             self.current_state = state
#             if state == "listening":
#                 self.target_radius = self.base_radius
#             elif state == "thinking":
#                 self.target_radius = self.base_radius * 1.1
#             else:
#                 self.target_radius = self.base_radius
#             self.pulse_value = 0.0
#             self.pulse_dir = 1
#             self.z_wobble = 0.0
#             self.z_dir = 1
#
#         # Smooth color
#         self.current_color += (self.target_color - self.current_color) * 0.05
#
#         # Pulse parameters
#         if self.current_state == "thinking":
#             pulse_speed = 0.001
#             pulse_strength = 0.001
#             z_speed = 0.001
#             z_strength = 0.005
#         elif self.current_state == "listening":
#             pulse_speed = 0.0000005
#             pulse_strength = 0.0000005
#             z_speed = 0.0005
#             z_strength = 0.002
#         else:
#             pulse_speed = 0
#             pulse_strength = 0
#             z_speed = 0
#             z_strength = 0
#             self.current_radius = self.base_radius
#             self.z_wobble = 0.0
#
#         # Update pulse
#         self.pulse_value += self.pulse_dir * pulse_speed
#         if self.pulse_value > pulse_strength or self.pulse_value < -pulse_strength:
#             self.pulse_dir *= -1
#         self.current_radius = self.target_radius + self.pulse_value
#
#         # Update z-axis wobble
#         self.z_wobble += self.z_dir * z_speed
#         if self.z_wobble > z_strength or self.z_wobble < -z_strength:
#             self.z_dir *= -1
#
#         # Rotate points
#         self.points = self.points @ self.rot_mat.T
#
#         # Apply radius and z wobble
#         scaled_points = self.points * self.current_radius
#         scaled_points[:, 2] += self.z_wobble
#
#         # Update scatter
#         self.scatter.set_data(scaled_points, face_color=self.current_color, size=self.BASE_SIZE)
#
#     def run(self):
#         app.run()





# class FaceController:
#     COLORS = {
#         "listening": np.array([0, 0, 1, 1], dtype=np.float32),
#         "thinking": np.array([0, 1, 0, 1], dtype=np.float32),
#         "error": np.array([1, 0, 0, 1], dtype=np.float32)
#     }
#
#     BASE_SIZE = 3
#     BASE_RADIUS = 1.0
#
#     def __init__(self):
#         self.state_queue = Queue()
#         self.command_queue = Queue()  # for sparkle events
#         self.current_color = self.COLORS["listening"].copy()
#         self.target_color = self.COLORS["listening"].copy()
#         self.n_points = 400
#         self.points = self.generate_points(self.n_points)
#
#         # Pulse / breathing
#         self.base_radius = self.BASE_RADIUS
#         self.current_radius = self.base_radius
#         self.target_radius = self.base_radius
#         self.pulse_value = 0.0
#         self.pulse_dir = 1
#         self.z_wobble = 0.0
#         self.z_dir = 1
#         self.current_state = "listening"
#
#         # Sparkle effect
#         self.sparkle_intensity = np.zeros(self.n_points, dtype=np.float32)  # 0=no sparkle
#         self.sparkle_decay = 0.05  # fade per frame
#
#         # SceneCanvas
#         self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
#                                         show=True, title="Jarvis AI Face")
#         self.view = self.canvas.central_widget.add_view()
#         self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
#         self.scatter = scene.visuals.Markers(parent=self.view.scene)
#         self.scatter.set_data(self.points, face_color=self.current_color, size=self.BASE_SIZE)
#
#         # Precompute rotation
#         self.angle = 0.01
#         c, s = np.cos(self.angle), np.sin(self.angle)
#         self.rot_mat = np.array([
#             [c, -s, 0],
#             [s,  c, 0],
#             [0,  0, 1]
#         ])
#
#         # Timer
#         self.timer = app.Timer(interval=1/60.0, connect=self.update, start=True)
#
#     def generate_points(self, n):
#         theta = np.random.uniform(0, 2*np.pi, n)
#         phi = np.random.uniform(0, np.pi, n)
#         r = np.random.uniform(0.5, 1.0, n)
#         x = r * np.sin(phi) * np.cos(theta)
#         y = r * np.sin(phi) * np.sin(theta)
#         z = r * np.cos(phi)
#         return np.c_[x, y, z]
#
#     def set_state(self, state: str):
#         if state in self.COLORS:
#             self.state_queue.put(state)
#
#     def sparkle(self):
#         """Trigger sparkle on ~10% of points near center."""
#         distances = np.linalg.norm(self.points, axis=1)
#         center_idx = np.where(distances < 0.6)[0]
#         sparkle_idx = np.random.choice(center_idx, max(1, len(center_idx)//10), replace=False)
#         self.sparkle_intensity[sparkle_idx] = 1.0  # full brightness
#
#     def update(self, event):
#         # Apply queued state changes
#         while not self.state_queue.empty():
#             state = self.state_queue.get()
#             self.target_color = self.COLORS[state].copy()
#             self.current_state = state
#             if state == "listening":
#                 self.target_radius = self.base_radius
#             elif state == "thinking":
#                 self.target_radius = self.base_radius * 1.1
#             else:
#                 self.target_radius = self.base_radius
#             self.pulse_value = 0.0
#             self.pulse_dir = 1
#             self.z_wobble = 0.0
#             self.z_dir = 1
#
#         # Smooth color
#         self.current_color += (self.target_color - self.current_color) * 0.05
#
#         # Pulse parameters
#         if self.current_state == "thinking":
#             pulse_speed = 0.05
#             pulse_strength = 0.03
#             z_speed = 0.01
#             z_strength = 0.05
#         elif self.current_state == "listening":
#             pulse_speed = 0.01
#             pulse_strength = 0.01
#             z_speed = 0.005
#             z_strength = 0.02
#         else:
#             pulse_speed = 0
#             pulse_strength = 0
#             z_speed = 0
#             z_strength = 0
#             self.current_radius = self.base_radius
#             self.z_wobble = 0.0
#
#         # Pulse
#         self.pulse_value += self.pulse_dir * pulse_speed
#         if self.pulse_value > pulse_strength or self.pulse_value < -pulse_strength:
#             self.pulse_dir *= -1
#         self.current_radius = self.target_radius + self.pulse_value
#
#         # Z-axis wobble
#         self.z_wobble += self.z_dir * z_speed
#         if self.z_wobble > z_strength or self.z_wobble < -z_strength:
#             self.z_dir *= -1
#
#         # Rotate points
#         self.points = self.points @ self.rot_mat.T
#
#         # Scale + wobble
#         scaled_points = self.points * self.current_radius
#         scaled_points[:, 2] += self.z_wobble
#
#         # Update sparkles (fade)
#         self.sparkle_intensity -= self.sparkle_decay
#         self.sparkle_intensity = np.clip(self.sparkle_intensity, 0, 1)
#
#         # Combine base color + sparkle
#         colors = np.tile(self.current_color, (self.n_points, 1))
#         colors[:, :3] += self.sparkle_intensity[:, np.newaxis] * 0.5  # brighten RGB
#         colors = np.clip(colors, 0, 1)
#
#         # Update scatter
#         self.scatter.set_data(scaled_points, face_color=colors, size=self.BASE_SIZE)
#
#     def run(self):
#         app.run()


# # modules/face.py
# from vispy import scene, app
# import numpy as np
# from queue import Queue
#
# class FaceController:
#     COLORS = {
#         "listening": np.array([0, 0, 1, 1], dtype=np.float32),
#         "thinking": np.array([0, 1, 0, 1], dtype=np.float32),
#         "error": np.array([1, 0, 0, 1], dtype=np.float32)
#     }
#
#     BASE_SIZE = 3
#     BASE_RADIUS = 1.0
#
#     def __init__(self):
#         self.state_queue = Queue()
#         self.current_color = self.COLORS["listening"].copy()
#         self.target_color = self.COLORS["listening"].copy()
#         self.n_points = 400  # fewer points = faster
#         self.points = self.generate_points(self.n_points)
#
#         # Pulse / breathing
#         self.base_radius = self.BASE_RADIUS
#         self.current_radius = self.base_radius
#         self.target_radius = self.base_radius
#         self.pulse_value = 0.0
#         self.pulse_dir = 1
#         self.current_state = "listening"
#
#         # SceneCanvas
#         self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
#                                         show=True, title="Jarvis AI Face")
#         self.view = self.canvas.central_widget.add_view()
#         self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
#         self.scatter = scene.visuals.Markers(parent=self.view.scene)
#         self.scatter.set_data(self.points, face_color=self.current_color, size=self.BASE_SIZE)
#
#         # Precompute rotation matrix
#         self.angle = 0.01
#         c, s = np.cos(self.angle), np.sin(self.angle)
#         self.rot_mat = np.array([
#             [c, -s, 0],
#             [s,  c, 0],
#             [0,  0, 1]
#         ])
#
#         # Timer for updates
#         self.timer = app.Timer(interval=1/60.0, connect=self.update, start=True)
#
#     def generate_points(self, n):
#         theta = np.random.uniform(0, 2*np.pi, n)
#         phi = np.random.uniform(0, np.pi, n)
#         r = np.random.uniform(0.5, 1.0, n)
#         x = r * np.sin(phi) * np.cos(theta)
#         y = r * np.sin(phi) * np.sin(theta)
#         z = r * np.cos(phi)
#         return np.c_[x, y, z]
#
#     def set_state(self, state: str):
#         if state in self.COLORS:
#             self.state_queue.put(state)
#
#     def update(self, event):
#         # Apply queued state changes
#         while not self.state_queue.empty():
#             state = self.state_queue.get()
#             self.target_color = self.COLORS[state].copy()
#             self.current_state = state
#             if state == "listening":
#                 self.target_radius = self.base_radius
#             elif state == "thinking":
#                 self.target_radius = self.base_radius * 1.1  # expand slightly
#             else:
#                 self.target_radius = self.base_radius
#             self.pulse_value = 0.0
#             self.pulse_dir = 1
#
#         # Smooth color transition
#         self.current_color += (self.target_color - self.current_color) * 0.05
#
#         # Smooth radius transition + pulse
#         if self.current_state == "thinking":
#             pulse_speed = 0.005
#             pulse_strength = 0.005
#         elif self.current_state == "listening":
#             pulse_speed = 0.0005
#             pulse_strength = 0.0005
#         else:
#             pulse_speed = 0
#             pulse_strength = 0
#             self.current_radius = self.base_radius
#
#         # Update pulse
#         self.pulse_value += self.pulse_dir * pulse_speed
#         if self.pulse_value > pulse_strength or self.pulse_value < -pulse_strength:
#             self.pulse_dir *= -1
#
#         self.current_radius = self.target_radius + self.pulse_value
#
#         # Rotate points in-place for speed
#         self.points = self.points @ self.rot_mat.T
#
#         # Apply 3D radius scaling
#         scaled_points = self.points * self.current_radius
#
#         # Update scatter
#         self.scatter.set_data(scaled_points, face_color=self.current_color, size=self.BASE_SIZE)
#
#     def run(self):
#         app.run()
#







# # modules/face.py
# from vispy import scene, app
# import numpy as np
# from queue import Queue
#
# class FaceController:
#     COLORS = {
#         "listening": np.array([0, 0, 1, 1], dtype=np.float32),  # blue
#         "thinking": np.array([0, 1, 0, 1], dtype=np.float32),   # green
#         "error": np.array([1, 0, 0, 1], dtype=np.float32)       # red
#     }
#
#     BASE_SIZE = 3  # base marker size
#
#     def __init__(self):
#         self.state_queue = Queue()
#         self.current_color = self.COLORS["listening"].copy()
#         self.target_color = self.COLORS["listening"].copy()
#         self.n_points = 500  # fewer points for performance
#         self.points = self.generate_points(self.n_points)
#
#         # Pulse parameters
#         self.base_scale = 1.0
#         self.pulse_scale = 0.0
#         self.pulse_direction = 1
#
#         # SceneCanvas
#         self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
#                                         show=True, title="Jarvis AI Face")
#         self.view = self.canvas.central_widget.add_view()
#         self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
#
#         # Particle markers
#         self.scatter = scene.visuals.Markers(parent=self.view.scene)
#         self.scatter.set_data(self.points, face_color=self.current_color, size=self.BASE_SIZE)
#
#         # Timer for rotation, color, and pulse
#         self.timer = app.Timer(interval=1/60.0, connect=self.update, start=True)
#
#         # Track current state
#         self.current_state = "listening"
#
#     def generate_points(self, n):
#         theta = np.random.uniform(0, 2*np.pi, n)
#         phi = np.random.uniform(0, np.pi, n)
#         r = np.random.uniform(0.5, 1.0, n)
#         x = r * np.sin(phi) * np.cos(theta)
#         y = r * np.sin(phi) * np.sin(theta)
#         z = r * np.cos(phi)
#         return np.c_[x, y, z]
#
#     def set_state(self, state: str):
#         if state in self.COLORS:
#             self.state_queue.put(state)
#
#     def update(self, event):
#         # Check for new state
#         while not self.state_queue.empty():
#             new_state = self.state_queue.get()
#             self.target_color = self.COLORS[new_state].copy()
#             self.current_state = new_state
#             # Reset pulse when state changes
#             self.pulse_scale = 0.0
#             self.pulse_direction = 1
#
#         # Smooth color shift
#         self.current_color += (self.target_color - self.current_color) * 0.05
#
#         # Rotate points
#         angle = 0.01
#         rot = np.array([
#             [np.cos(angle), -np.sin(angle), 0],
#             [np.sin(angle),  np.cos(angle), 0],
#             [0, 0, 1]
#         ])
#         self.points = self.points @ rot.T
#
#         # Pulse effect
#         if self.current_state == "thinking":
#             # Faster, stronger pulse
#             self.pulse_scale += self.pulse_direction * 0.05
#             if self.pulse_scale > 0.3 or self.pulse_scale < 0:
#                 self.pulse_direction *= -1
#         elif self.current_state == "listening":
#             # Slow, subtle shrink-expand
#             self.pulse_scale += self.pulse_direction * 0.01
#             if self.pulse_scale > 0.1 or self.pulse_scale < -0.1:
#                 self.pulse_direction *= -1
#         else:
#             self.pulse_scale = 0.0  # no pulse on error
#
#         size = self.BASE_SIZE * (self.base_scale + self.pulse_scale)
#         self.scatter.set_data(self.points, face_color=self.current_color, size=size)
#
#     def run(self):
#         app.run()
#
#
#
#
# # from vispy import scene, app
# # import vispy
# # import numpy as np
# # from queue import Queue
# #
# #
# # class FaceController:
# #     vispy.use('PyQt6')
# #
# #     COLORS = {
# #         "listening": 'blue',
# #         "thinking": 'green',
# #         "error": 'red'
# #     }
# #
# #     def __init__(self):
# #         self.state_queue = Queue()
# #         self.state = "listening"
# #         self.n_points = 500  # make less if laggy - add more for better visuals
# #         self.points = self.generate_points(self.n_points)
# #
# #         # SceneCanvas
# #         self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
# #                                         show=True, title="Jarvis AI Face")
# #         self.view = self.canvas.central_widget.add_view()
# #         self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)
# #
# #         # Particle markers
# #         self.scatter = scene.visuals.Markers(parent=self.view.scene)
# #         self.scatter.set_data(self.points, face_color=self.COLORS[self.state], size=3)
# #
# #         # Timer for animation & state polling
# #         self.timer = app.Timer(interval=1 / 120.0, connect=self.update, start=True)
# #
# #     def generate_points(self, n):
# #         theta = np.random.uniform(0, 2 * np.pi, n)
# #         phi = np.random.uniform(0, np.pi, n)
# #         r = np.random.uniform(0.5, 1.0, n)
# #         x = r * np.sin(phi) * np.cos(theta)
# #         y = r * np.sin(phi) * np.sin(theta)
# #         z = r * np.cos(phi)
# #         return np.c_[x, y, z]
# #
# #     def set_state(self, state: str):
# #         # Instead of changing immediately, enqueue state
# #         if state in self.COLORS:
# #             self.state_queue.put(state)
# #
# #     def update(self, event):
# #         # Apply state changes from queue
# #         while not self.state_queue.empty():
# #             self.state = self.state_queue.get()
# #
# #         # Rotate points
# #         angle = 0.01
# #         rot = np.array([
# #             [np.cos(angle), -np.sin(angle), 0],
# #             [np.sin(angle), np.cos(angle), 0],
# #             [0, 0, 1]
# #         ])
# #         self.points = self.points @ rot.T
# #         self.scatter.set_data(self.points, face_color=self.COLORS[self.state], size=5)
# #
# #     def run(self):
# #         app.run()
