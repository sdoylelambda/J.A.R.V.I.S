import pyttsx3


class Awareness:
    def __init__(self):
        print("Observer initialized.")

    def listen(self):
        return input("Simulated STT input: ")

    def listen_confirmation(self):
        resp = input("Approve plan? (y/n): ")
        return resp.lower() in ['y','yes']

    def speak(self, text):
        print(f"Jarvis says: {text}")
        engine = pyttsx3.init()

        # Jarvis-like tuning
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)  # try 0 or 1

        engine.say(f"Systems online. {text}, correct?")
        engine.runAndWait()
