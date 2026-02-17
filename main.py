from modules.face import FaceController
from modules.window_controller import WindowController
from modules.observer import Observer
import threading


if __name__ == "__main__":
    face = FaceController()
    window_controller = WindowController()

    observer_thread = threading.Thread(target=lambda: Observer(face, window_controller).listen_and_respond(), daemon=True)
    observer_thread.start()

    face.run()














# def main():
#     # 1️⃣ Initialize Observer
#     observer = Observer(config_path="config.yaml")
#
#     print("[Observer] Listening and responding...")
#
#     try:
#         # 2️⃣ Stream from mic (short & long chunks)
#         for text in observer.ears.listen_stream(short_chunk_sec=1.0, long_chunk_sec=5.0):
#             if text:
#                 print(f"[Heard]: {text}")
#
#                 # 3️⃣ Handle short commands
#                 observer.launcher.open_app(text)
#
#                 # 4️⃣ Speak the transcribed text
#                 observer.mouth.speak(text)
#
#     except KeyboardInterrupt:
#         print("\n[Observer] Stopped by user.")
#     finally:
#         observer.running = False
#         print("[Observer] Shutting down.")
#
# if __name__ == "__main__":
#     main()









# from modules.observer import Observer
# from modules.app_launcher import AppLauncher
#
#
# def main():
#     # Where should while loop be? Here or below?
#
#     print("Jarvis starting...")
#     # observer = Observer()
#     #
#     # while True:
#     #     observer.listen_and_speak()
#         # text = observer.listen()
#         # print("[Heard]:", text)
#
# if __name__ == "__main__":
#     jarvis = Observer()
#
#     print("\n[Jarvis] Ready. Speak now. Press Ctrl+C to stop.\n")
#     try:
#         while True:
#             jarvis.listen_and_respond()
#     except KeyboardInterrupt:
#         print("\n[Jarvis] Exiting.")










# import time
# # from modules.stt import STT        # updated Ears class with Whisper
# from modules.tts import TTSModule  # your updated Mouth class
# from modules.brain import Brain
# from modules.hands import Hands
# from modules.observer import Observer
# from modules.app_launcher import AppLauncher
#
#
# def main(self):
#     print("Jarvis starting...")
#     # Real STT/TTS
#     observer = Observer()
#     ears = observer.listen(audio)
#     mouth = TTSModule(use_mock=False)
#     brain = Brain()
#     hands = Hands()
#     observer = Observer()
#     launcher = AppLauncher()
#
#     print("Jarvis running... Say 'exit' to quit.")
#
#     while True:
#         # Listen for an intent
#         print("[Observer] Waiting for intent...")
#         try:
#             spoken_text = ears.ears()  # records and transcribes audio
#         except Exception as e:
#             print(f"[Ears] Error capturing audio: {e}")
#             time.sleep(0.5)
#             continue
#
#         if not spoken_text:
#             print("[Ears] Nothing detected, continuing...")
#             time.sleep(0.5)
#             continue
#
#         print(f"[Observer] Heard: {spoken_text}")
#
#         if spoken_text.lower() in ["exit", "quit", "stop"]:
#             print("Exiting...")
#             break
#
#         # Voice command to open apps
#         if "open " in spoken_text.lower():
#             app_name = spoken_text.lower().replace("open ", "").strip()
#             launcher.open_app(app_name)
#             continue  # Skip the rest of loop for now
#
#         # if spoken_text.lower() in ["open pycharm"]:
#         #     print("Opening pycharm...")
#         #     open(pycharm)
#
#         observer.speak(f"You said: {spoken_text}")
#
#         # Create plan based on intent
#         plan = brain.create_plan(spoken_text)
#         observer.speak(plan['summary'])
#
#         # Ask for approval
#         approval = observer.listen_confirmation()
#         if approval:
#             hands.execute(plan)
#         else:
#             observer.speak("Plan cancelled.")
#
#
# if __name__ == "__main__":
#     main(self=any)






















# import time
# from modules.stt import STT        # your updated Ears class
# from modules.tts import TTSModule  # your updated Mouth class
# from modules.brain import Brain
# from modules.hands import Hands
# from modules.observer import Observer
#
#
# def main():
#     print("Jarvis starting...")
#     # Real STT/TTS
#     ears = STT(use_mock=False, mic_index=0)
#     mouth = TTSModule(use_mock=False)
#     brain = Brain()
#     hands = Hands()
#     observer = Observer()
#
#     print("Jarvis running... Say 'exit' to quit.")
#
#     while True:
#         # Listen for an intent
#         print("[Observer] Waiting for intent...")
#         intent = observer.listen()
#         if not intent:
#             # Nothing heard, continue listening
#             continue
#
#         if intent.lower() in ["exit", "quit", "stop"]:
#             print("Exiting...")
#             break
#
#         observer.speak(f"You said: {intent}")
#
#         # Create plan based on intent
#         plan = brain.create_plan(intent)
#         observer.speak(plan['summary'])
#
#         # Ask for approval
#         approval = observer.listen_confirmation()
#         if approval:
#             hands.execute(plan)
#         else:
#             observer.speak("Plan cancelled.")
#
# if __name__ == "__main__":
#     main()
    # Speach test - Can Jarvis hear?
    # r = sr.Recognizer()
    # mic_index = 0  # card 0 device 0
    # with sr.Microphone(device_index=mic_index) as source:
    #     print("Speak something now...")
    #     r.adjust_for_ambient_noise(source, duration=1)
    #     audio = r.listen(source, timeout=10)
    #     try:
    #         text = r.recognize_google(audio)
    #         print("You said:", text)
    #     except Exception as e:
    #         print("Error:", e)




    # print("Jarvis MVP (single-node) running...")
#
#     while True:
#         # Observer listens for intent
#         intent = observer.listen()
#         if not intent:
#             time.sleep(0.5)
#             continue
#
#         # --- LIVE SPEECH INPUT ---
#         spoken_text = ears.ears()  # now uses microphone
#         if spoken_text.lower() in ["exit", "quit", "stop"]:
#             print("Exiting...")
#             break
#
#         # Speak back what was heard
#         mouth.speak(spoken_text, play_audio=True)
#
#         # Brain processes the intent
#         plan = brain.create_plan(intent)
#         observer.speak(plan['summary'])
#
#         # Observer asks for approval
#         approval = observer.listen_confirmation()
#         if approval:
#             hands.execute(plan)
#         else:
#             observer.speak("Plan cancelled.")
#
# if __name__ == "__main__":
#     main()



# from modules.brain import Brain
# from modules.hands import Hands
# from modules.observer import Observer
# import time
#
# def main():
#     brain = Brain()
#     hands = Hands()
#     observer = Observer()
#     print("Jarvis MVP (single-node) running...")
#     while True:
#         intent = observer.listen()
#         if not intent:
#             time.sleep(0.5)
#             continue
#         plan = brain.create_plan(intent)
#         observer.speak(plan['summary'])
#         approval = observer.listen_confirmation()
#         if approval:
#             hands.execute(plan)
#         else:
#             observer.speak("Plan cancelled.")
#
# if __name__ == "__main__":
#     main()


# from modules.brain import Brain
# from modules.hands import Hands
# from modules.ears import Ears
# from modules.mouth import Mouth
# from modules.awareness import Awareness
# import time
#
#
# def main():
#     brain = Brain()
#     hands = Hands()
#     awareness = Awareness()
#     print("Jarvis (single-node) running...")
#
#     while True:
#         intent = awareness.listen()
#
#         if not intent:
#             time.sleep(0.5)
#             continue
#
#         plan = brain.create_plan(intent)
#         awareness.speak(plan['summary'])
#         approval = awareness.listen_confirmation()
#
#         if approval:
#             awareness.speak(plan['summary'])
#             hands.execute(plan)
#         else:
#             awareness.speak("Plan cancelled.")
#
#
# if __name__ == "__main__":
#     main()
