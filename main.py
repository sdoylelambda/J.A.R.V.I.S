import threading
from queue import Queue
from modules.face import FaceController
from modules.window_controller import WindowController
from modules.app_launcher import AppLauncher
from modules.observer import Observer
from modules.browser_controller import BrowserController

if __name__ == "__main__":
    # -----------------------------
    # Initialize Face & Controllers
    # -----------------------------
    face = FaceController()
    window_controller = WindowController()
    browser_controller = BrowserController()
    launcher = AppLauncher(window_controller)

    # -----------------------------
    # Observer with browser queue
    # -----------------------------
    observer = Observer(face, window_controller, launcher)

    # -----------------------------
    # Browser thread for async commands
    # -----------------------------
    browser_thread = threading.Thread(
        target=browser_controller.process_queue,
        daemon=True
    )
    browser_thread.start()

    # -----------------------------
    # Observer listens and responds
    # -----------------------------
    observer_thread = threading.Thread(
        target=observer.listen_and_respond,
        daemon=True
    )
    observer_thread.start()

    # -----------------------------
    # Run Face GUI (blocking)
    # -----------------------------
    face.run()



























# # main.py
# from modules.face import FaceController
# from modules.window_controller import WindowController
# from modules.app_launcher import AppLauncher
# from modules.ears import Ears
# from modules.stt import STT
# from modules.tts import TTSModule
# from modules.observer import Observer
# import threading
# import queue
#
#
# # ------------------------
# # Process browser commands safely on main thread
# # ------------------------
# browser_queue = queue.Queue()
#
# def process_browser_queue(app_launcher):
#     try:
#         while True:
#             command = browser_queue.get_nowait()
#             print(f"[BrowserController] Received: {command}")
#             app_launcher.handle_command(command)
#     except queue.Empty:
#         pass
#     # Check again after 50ms
#     threading.Timer(0.05, process_browser_queue, args=(app_launcher,)).start()
#
# if __name__ == "__main__":
#     face = FaceController()
#     window_controller = WindowController()
#     launcher = AppLauncher(window_controller)
#     ears = Ears()
#     mouth = STT()
#     stt = TTSModule()
#     # ears, mouth, stt objects assumed initialized somewhere
#     observer = Observer(face, window_controller, launcher, queue)
#
#     observer_thread = threading.Thread(
#         target=observer.listen_and_respond,
#         daemon=True
#     )
#     observer_thread.start()
#
#     face.run()
#
#
#
#
#






# import threading
# import queue
# from modules.face import FaceController
# from modules.window_controller import WindowController
# from modules.app_launcher import AppLauncher
# from modules.observer import Observer
#
# # ------------------------
# # Global browser queue
# # ------------------------
# browser_queue = queue.Queue()
#
# # ------------------------
# # Process browser commands safely on main thread
# # ------------------------
# def process_browser_queue(app_launcher):
#     try:
#         while True:
#             command = browser_queue.get_nowait()
#             print(f"[BrowserController] Received: {command}")
#             app_launcher.handle_command(command)
#     except queue.Empty:
#         pass
#     # Check again after 50ms
#     threading.Timer(0.05, process_browser_queue, args=(app_launcher,)).start()
#
#
# # ------------------------
# # Main entry
# # ------------------------
# if __name__ == "__main__":
#     face = FaceController()
#     window_controller = WindowController()
#     launcher = AppLauncher()
#
#     # Pass browser_queue into Observer
#     observer = Observer(face, window_controller, launcher, browser_queue)
#
#     observer_thread = threading.Thread(
#         target=observer.listen_and_respond,
#         daemon=True
#     )
#     observer_thread.start()
#
#     # Start recurring browser queue processing
#     process_browser_queue(launcher)
#
#     # GUI must stay on main thread
#     face.run()













# from modules.face import FaceController
# from modules.window_controller import WindowController
# from modules.app_launcher import AppLauncher
# from modules.observer import Observer
# import threading
# import queue
#
# browser_queue = queue.Queue()
#
#
# if __name__ == "__main__":
#     face = FaceController()
#
#     window_controller = WindowController()
#     launcher = AppLauncher()
#
#     observer = Observer(face, window_controller, launcher)
#
#     observer_thread = threading.Thread(
#         target=observer.listen_and_respond,
#         daemon=True
#     )
#     observer_thread.start()
#
#     face.run()   # GUI MUST stay on main thread































# import time
# from modules.app_launcher import AppLauncher
# from modules.tts import TTS
# from modules.ears import Ears
#
# def main():
#     # Initialize components
#     tts = TTS()
#     ears = Ears()
#     launcher = AppLauncher()
#
#     # Greet user
#     tts.speak("Hello sir, what can I do for you?")
#
#     while True:
#         try:
#             # 1️⃣ Listen
#             spoken_text = ears.listen(duration=5)  # adjust duration as needed
#             if not spoken_text:
#                 continue
#
#             print(f"[Heard]: {spoken_text}")
#
#             # 2️⃣ Handle command
#             handled = launcher.handle_command(spoken_text)
#
#             # 3️⃣ Give feedback
#             if not handled:
#                 tts.speak("Command not recognized.")
#             else:
#                 tts.speak("Command executed.")
#
#             # Small delay to avoid overlapping commands
#             time.sleep(0.5)
#
#         except KeyboardInterrupt:
#             print("Exiting J.A.R.V.I.S...")
#             break
#         except Exception as e:
#             print(f"[Error] {e}")
#             tts.speak("An error occurred.")
#
# if __name__ == "__main__":
#     main()
















# from modules.face import FaceController
# from modules.window_controller import WindowController
# from modules.app_launcher import AppLauncher
# from modules.observer import Observer
# import threading
#
#
# if __name__ == "__main__":
#     face = FaceController()
#
#     window_controller = WindowController()
#     launcher = AppLauncher(window_controller)
#
#     observer = Observer(face, window_controller, launcher)
#
#     observer_thread = threading.Thread(
#         target=observer.listen_and_respond,
#         daemon=True
#     )
#     observer_thread.start()
#
#     face.run()
#

