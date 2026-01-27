import pyttsx3
from brain import Brain
from hands import Hands
from ears import Ears
from mouth import Mouth


class Awareness:
    def __init__(self):
        self.stt = Ears()
        self.tts = Mouth()
        print("Observer initialized.")

    def listen(self):
        # return input("Simulated STT input: ")

        audio_path = input("Simulated audio path or text: ")
        # For real mic: integrate PyAudio
        return self.stt.transcribe(audio_path)

    def listen_confirmation(self):
        resp = input("Approve plan? (y/n): ")
        return resp.lower() in ['y','yes']

    def speak(self, text):
        print(f"Jarvis says: {text}")

        self.tts.speak(text)

        engine = pyttsx3.init()

        # Jarvis-like tuning
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)  # try 0 or 1

        engine.say(f"Systems online. {text}, correct?")
        engine.runAndWait()
