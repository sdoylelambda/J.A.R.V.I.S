# from TTS.api import TTS
# import simpleaudio as sa
# import sys, os
# sys.path.insert(0, os.path.dirname(__file__))

class Mouth:
    def __init__(self):
        print("Loading TTS model...")
        # self.tts = TTS(model_name)
        print("TTS mock initialized.")

    def speak(self, text):
        print(f"[TTS] {text}")
        # self.tts.tts_to_file(text=text, file_path="tts_output.wav")
        # Optional: auto-play
        # wave_obj = sa.WaveObject.from_wave_file("tts_output.wav")
        # play_obj = wave_obj.play()
        # play_obj.wait_done()
