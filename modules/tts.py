from TTS.api import TTS
import simpleaudio as sa

class TTSModule:
    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False):
        print("Loading TTS model...")
        self.tts = TTS(model_name)

    def speak(self, text):
        self.tts.tts_to_file(text=text, file_path="tts_output.wav")
        # Optional: auto-play
        wave_obj = sa.WaveObject.from_wave_file("tts_output.wav")
        play_obj = wave_obj.play()
        play_obj.wait_done()



# class TTSModule:
#     def __init__(self):
#         print("TTS mock initialized.")
#
#     def speak(self, text):
#         print(f"[TTS] {text}")



# from TTS.api import TTS
# import simpleaudio as sa
#
# class Mouth:
#     def __init__(self):
#         print("Loading TTS model...")
#         self.tts = TTS(model_name)
#         print("TTS mock initialized.")
#
#     def speak(self, text):
#         print(f"[TTS] {text}")
#         self.tts.tts_to_file(text=text, file_path="tts_output.wav")
#         # Optional: auto-play
#         # wave_obj = sa.WaveObject.from_wave_file("tts_output.wav")
#         # play_obj = wave_obj.play()
#         # play_obj.wait_done()
