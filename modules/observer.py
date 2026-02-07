from modules.stt import STT
from modules.tts import TTSModule
from modules.brain import Brain
from modules.hands import Hands
import time


class Observer:
    def __init__(self):
        self.stt = STT(use_mock=False)
        self.tts = TTSModule()
        print("Observer initialized.")

    def listen(self):
        # audio_path = input("Simulated audio path or text: ")
        # For real mic: integrate PyAudio
        # return self.stt.transcribe(audio_path)
        return self.stt.ears()

    def listen_confirmation(self):
        print("[Observer] Awaiting confirmation (yes/no)...")
        response = self.stt.ears()
        if response:
            return response.lower() in ["yes", "yep", "affirmative"]
        return False

    def speak(self, text):
        print(f"Jarvis says: {text}")
        self.tts.speak(text, play_audio=True)






# import pyttsx3
# from modules.brain import Brain
# from modules.hands import Hands
# from modules.ears import Ears
# from modules.mouth import Mouth


# class Observer:
#     def __init__(self):
#         print("Observer initialized.")
#
#     def listen(self):
#         return input("Simulated STT input: ")
#
#     def listen_confirmation(self):
#         resp = input("Approve plan? (y/n): ")
#         return resp.lower() in ['y','yes']
#
#     def speak(self, text):
#         print(f"Jarvis says: {text}")



# class Observer:
#     def __init__(self):
#         self.stt = Ears()
#         self.tts = Mouth()
#         print("Observer initialized.")
#
#     def listen(self):
#         # return input("Simulated STT input: ")
#
#         audio_path = input("Simulated audio path or text: ")
#         # For real mic: integrate PyAudio
#         return self.stt.transcribe(audio_path)
#
#     def listen_confirmation(self):
#         resp = input("Approve plan? (y/n): ")
#         return resp.lower() in ['y','yes']
#
#     def speak(self, text):
#         print(f"Jarvis says: {text}")
#
#         self.tts.speak(text)
#
#         engine = pyttsx3.init()
#
#         # Jarvis-like tuning
#         engine.setProperty("rate", 175)
#         engine.setProperty("volume", 1.0)
#
#         voices = engine.getProperty("voices")
#         engine.setProperty("voice", voices[0].id)  # try 0 or 1
#
#         engine.say(f"Systems online. {text}, correct?")
#         engine.runAndWait()
