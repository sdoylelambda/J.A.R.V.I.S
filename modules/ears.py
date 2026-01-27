# import whisper

class Ears:
    def __init__(self):
        print("STT mock initialized.")
        # self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path=None):
        return input("Simulated audio transcription: ")
