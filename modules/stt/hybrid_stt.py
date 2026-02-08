import os
import subprocess
import shlex
import sounddevice as sd
import numpy as np
import simpleaudio as sa
import yaml
import whisper
from modules.stt.faster_whisper_stt import WhisperModel
from TTS.api import TTS


# -----------------------------
# Hybrid STT (Whisper + Faster Whisper)
# -----------------------------
class HybridSTT:
    def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
        # Whisper for short commands
        self.whisper_model = whisper.load_model(whisper_model, device="cuda" if use_gpu else "cpu")

        # Faster Whisper for long audio
        device = "cuda" if use_gpu else "cpu"
        self.fw_model = WhisperModel(fw_model, device=device, compute_type="int8")

        self.samplerate = 16000

    def transcribe(self, audio_array):
        duration_sec = len(audio_array) / self.samplerate

        if duration_sec < 3:
            # Short command → Whisper
            audio_float = audio_array.astype(np.float32) / 32768.0
            result = self.whisper_model.transcribe(audio_float, language="en")
            return result["text"]
        else:
            # Long dictation → Faster Whisper
            if audio_array.ndim > 1:
                audio_array = audio_array.mean(axis=1)
            audio_float = audio_array.astype(np.float32) / 32768.0
            segments, _ = self.fw_model.transcribe(
                audio_float,
                language="en",
                temperature=0.0,
                suppress_blank=True,
                word_timestamps=False,
                beam_size=1,
            )
            return " ".join([seg.text for seg in segments])
