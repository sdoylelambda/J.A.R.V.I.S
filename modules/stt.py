import whisper
import os


class STT:
    def __init__(self):
        self.model = whisper.load_model("base", device="cpu")

    def transcribe(self, input_data):
        # Case 1: real audio file
        if (
            isinstance(input_data, str)
            and os.path.isfile(input_data)
            and input_data.lower().endswith((".wav", ".mp3", ".flac", ".m4a", ".ogg"))
        ):
            result = self.model.transcribe(input_data)
            return result["text"]

        # Case 2: already text (simulation / CLI / test)
        if isinstance(input_data, str):
            return input_data

        raise ValueError(f"Unsupported STT input: {type(input_data)}")



# class Ears:
#     def __init__(self):
#         print("STT mock initialized.")
#         # self.model = whisper.load_model(model_name)
#
#     def transcribe(self, audio_path=None):
#         return input("Simulated audio transcription: ")
