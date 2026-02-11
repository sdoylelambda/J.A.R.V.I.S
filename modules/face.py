from vispy import scene, app
import vispy
import numpy as np
from queue import Queue


class FaceController:
    vispy.use('PyQt6')

    canvas = scene.SceneCanvas(keys='interactive', size=(400, 400), show=True)
    canvas.app.run()
    COLORS = {
        "listening": 'blue',
        "thinking": 'green',
        "error": 'red'
    }

    def __init__(self):
        self.state_queue = Queue()
        self.state = "listening"
        self.n_points = 1000
        self.points = self.generate_points(self.n_points)

        # SceneCanvas
        self.canvas = scene.SceneCanvas(keys='interactive', size=(600, 600),
                                        show=True, title="Jarvis AI Face")
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.cameras.TurntableCamera(fov=45, distance=4)

        # Particle markers
        self.scatter = scene.visuals.Markers(parent=self.view.scene)
        self.scatter.set_data(self.points, face_color=self.COLORS[self.state], size=5)

        # Timer for animation & state polling
        self.timer = app.Timer(interval=1 / 60.0, connect=self.update, start=True)

    def generate_points(self, n):
        theta = np.random.uniform(0, 2 * np.pi, n)
        phi = np.random.uniform(0, np.pi, n)
        r = np.random.uniform(0.5, 1.0, n)
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
        return np.c_[x, y, z]

    def set_state(self, state: str):
        # Instead of changing immediately, enqueue state
        if state in self.COLORS:
            self.state_queue.put(state)

    def update(self, event):
        # Apply state changes from queue
        while not self.state_queue.empty():
            self.state = self.state_queue.get()

        # Rotate points
        angle = 0.01
        rot = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        self.points = self.points @ rot.T
        self.scatter.set_data(self.points, face_color=self.COLORS[self.state], size=5)

    def run(self):
        app.run()
