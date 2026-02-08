from modules.stt.factory import create_stt
from modules.stt.faster_whisper_stt import FasterWhisperSTT
from modules.stt.hybrid_stt import HybridSTT
from modules.app_launcher import AppLauncher
from modules.tts import TTSModule
from modules.ears import Ears
import yaml


# Rename as Jarvis?
class Observer:
    def __init__(self, config_file="config.yaml"):
        with open(config_file) as f:
            config = yaml.safe_load(f)

        use_gpu = config["system"].get("use_gpu", False)
        self.stt = HybridSTT(
            whisper_model=config["stt"].get("whisper_model", "small"),
            fw_model=config["stt"].get("fw_model", "small"),
            use_gpu=use_gpu
        )
        self.ears = Ears(self.stt, mic_index=config["audio"].get("mic_index", 0),
                         duration=config["audio"].get("duration", 3))
        self.tts = TTSModule(gpu=use_gpu)
        self.launcher = AppLauncher()

    def listen_and_respond(self):
        text = self.ears.listen()
        text = text.strip()
        if not text:
            return

        print(f"[Heard]: {text}")

        # Check for app commands first
        if self.launcher.open_app(text):
            self.tts.speak(f"Opening {text}")
        else:
            self.tts.speak(text)














    # def __init__(self, config_file="config.yaml"):
    #     with open(config_file) as f:
    #         config = yaml.safe_load(f)
    #
    #     # Initialize STT engine
    #     engine = config["transcription"]["engine"].lower()
    #     if engine == "faster-whisper":
    #         self.stt = FasterWhisperSTT(config)
    #     else:
    #         raise ValueError(f"Unknown STT engine: {engine}")
    #
    #     # Microphone listener
    #     self.ears = Ears(self.stt, use_mock=config["audio"].get("use_mock", False))
    #
    #     # TTS
    #     self.tts = TTSModule(
    #         use_mock=config["audio"].get("use_mock", False),
    #         gpu=config["system"].get("use_gpu", False)
    #     )
    #
    # def listen_and_speak(self):
    #     text = self.ears.listen()
    #     if len(text.strip()) < 2:
    #         print("[Jarvis] Ignored too short input.")
    #     else:  # refactor this
    #         if text.strip():
    #             print(f"[Heard]: {text}")
    #             self.tts.speak(text)










# class Observer:
#     def __init__(self, config_file="config.yaml"):
#         with open(config_file) as f:
#             config = yaml.safe_load(f)
#
#         engine = config["transcription"]["engine"].lower()
#         if engine == "faster_whisper":
#             self.stt = FasterWhisperSTT(config)
#         elif engine == "whisper":
#             self.stt = WhisperSTT(config)
#         else:
#             raise ValueError(f"Unknown STT engine: {engine}")
#
#         self.ears = Ears(self.stt, use_mock=config["audio"].get("use_mock", False))
#         self.tts = TTSModule(
#             use_mock=config["audio"].get("use_mock", False),
#             gpu=config["system"].get("use_gpu", False)
#         )
#
#     def listen_and_speak(self):
#         text = self.ears.listen()
#         if text:
#             print(f"[Heard]: {text}")
#             self.tts.speak(text)

# class Observer:
#     def __init__(self):
#         with open("config.yaml") as f:
#             config = yaml.safe_load(f)
#
#         self.stt = create_stt(config)
#         self.ears = Ears(
#             stt=self.stt,
#             samplerate=config["audio"]["samplerate"],
#             duration=config["audio"]["duration"],
#             mic_index=config["audio"].get("mic_index"),
#             use_mock=config["audio"].get("use_mock", False),
#         )
#
#     def listen(self):
#         return self.ears.listen()





# from modules.stt.__init__ import create_stt
# import yaml
# from modules.brain import Brain
# from modules.hands import Hands
# import time
#
#
# class Observer:
#     def __init__(self):
#         with open("config.yaml") as f:
#             config = yaml.safe_load(f)
#
#         self.stt = create_stt(config)
#         print("Observer initialized.")
#
#     def listen(self, audio):
#         # audio_path = input("Simulated audio path or text: ")
#         # For real mic: integrate PyAudio
#         # return self.stt.transcribe(audio_path)
#         # return self.stt.ears()
#         return self.stt.transcribe(audio)
#
#     def listen_confirmation(self):
#         print("[Observer] Awaiting confirmation (yes/no)...")
#         response = self.stt.ears()
#         if response:
#             return response.lower() in ["yes", "yep", "affirmative"]
#         return False
#
#     def speak(self, text):
#         print(f"Jarvis says: {text}")
#         self.tts.speak(text, play_audio=True)
#
#




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
