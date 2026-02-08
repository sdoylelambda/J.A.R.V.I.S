class BaseSTT:
    def transcribe(self, audio_bytes):
        raise NotImplementedError
