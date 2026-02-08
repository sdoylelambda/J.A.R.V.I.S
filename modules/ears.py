import os
import sounddevice as sd
import numpy as np
# import wavio  # for saving WAV files if needed
from modules.stt.factory import create_stt  # assuming your factory is in stt/factory.py
from scipy.io.wavfile import write


class Ears:
    """
    Microphone interface for recording and transcribing audio.
    Supports both Whisper and FasterWhisper via the STTFactory.
    """

    def __init__(self, stt, samplerate=16000, duration=5, mic_index=None, use_mock=False):        # STT engine
        # self.stt = create_stt(config)
        #
        # # Audio settings
        # self.samplerate = 16000
        # self.duration = config["stt"]["duration"]
        # self.mic_index = 0
        # self.use_mock = use_mock
        self.stt = stt
        self.samplerate = samplerate
        self.duration = duration
        self.mic_index = mic_index
        self.use_mock = use_mock

    def listen(self, duration=None, filename="capture.wav"):
        """
        Record audio from the microphone and return transcribed text.
        """
        if self.use_mock:
            return input("Simulated audio: ")

        duration = duration or self.duration
        print("[Ears] Listening... Please speak now.")

        # Record audio
        audio = sd.rec(
            int(duration * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype="int16",
            device=self.mic_index,
        )
        sd.wait()

        # Save audio to WAV file (optional, useful for FasterWhisper)
        # wavio.write(filename, audio, self.samplerate, sampwidth=2)
        write(filename, self.samplerate, audio)

        print("[Ears] Processing transcription...")
        text = self.stt.transcribe(filename)
        return text




# import sounddevice as sd
# from scipy.io.wavfile import write
#
# class Ears:
#     def __init__(self, stt, samplerate=16000, duration=5, mic_index=None, use_mock=False):
#         self.stt = stt
#         self.samplerate = samplerate
#         self.duration = duration
#         self.mic_index = mic_index
#         self.use_mock = use_mock
#
#     def listen(self, duration=None, filename="capture.wav"):
#         """Record audio from microphone and return transcribed text."""
#         if self.use_mock:
#             return input("Simulated audio: ")
#
#         duration = duration or self.duration
#         print("[Ears] Listening... Please speak now.")
#
#         audio = sd.rec(
#             int(duration * self.samplerate),
#             samplerate=self.samplerate,
#             channels=1,
#             dtype="int16",
#             device=self.mic_index,
#         )
#         sd.wait()
#
#         write(filename, self.samplerate, audio)
#
#         return self.stt.transcribe(filename)
