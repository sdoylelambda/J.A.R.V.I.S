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
