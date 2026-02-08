import whisper
from faster_whisper import WhisperModel


class HybridSTT:
    def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
        device = "cuda" if use_gpu else "cpu"

        print("[STT] Loading Whisper...")
        self.whisper = whisper.load_model(whisper_model, device=device)

        print("[STT] Loading Faster-Whisper...")
        self.faster = WhisperModel(
            fw_model,
            device=device,
            compute_type="int8" if not use_gpu else "float16"
        )

    def transcribe_short(self, audio_path):
        result = self.whisper.transcribe(
            audio_path,
            language="en",
            temperature=0.0,
            no_speech_threshold=0.6,
            logprob_threshold=-1.0
        )
        return result.get("text", "").strip()

    def transcribe_long(self, audio_path):
        segments, _ = self.faster.transcribe(
            audio_path,
            language="en",
            beam_size=1,
            vad_filter=True
        )
        return " ".join(seg.text for seg in segments).strip()











# modules/stt/hybrid_stt.py
# import whisper
# import numpy as np
# from faster_whisper import WhisperModel
#
# class HybridSTT:
#     def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
#         self.use_gpu = use_gpu
#
#         # Whisper CPU (short commands ≤5s)
#         device = "cpu"
#         print(f"[STT] Loading Whisper model '{whisper_model}' on CPU for short commands...")
#         self.whisper_model = whisper.load_model(whisper_model, device=device)
#         print("[STT] Whisper loaded.")
#
#         # Faster Whisper int8 (long dictation >5s)
#         device_fw = "cuda" if use_gpu else "cpu"
#         print(f"[STT] Loading Faster Whisper model '{fw_model}' on {device_fw} for long dictation...")
#         self.fw_model = WhisperModel(fw_model, device=device_fw, compute_type="int8")
#         print("[STT] Faster Whisper loaded.")
#
#     def transcribe_short(self, audio_file):
#         """Use Whisper CPU for short commands (≤5s)"""
#         try:
#             result = self.whisper_model.transcribe(audio_file, language="en")
#             text = result.get("text", "").strip()
#             return text
#         except Exception as e:
#             print(f"[STT][Whisper] Error: {e}")
#             return ""
#
#     def transcribe_long(self, audio_array, beam_size=1):
#         """Use Faster Whisper int8 for long dictation (>5s)"""
#         if audio_array.ndim > 1:
#             audio_array = audio_array.mean(axis=1)  # mono
#         audio_float = audio_array.astype(np.float32) / 32768.0
#         try:
#             segments, _ = self.fw_model.transcribe(
#                 audio_float,
#                 language="en",
#                 temperature=0.0,
#                 suppress_blank=True,
#                 word_timestamps=False,
#                 beam_size=beam_size
#             )
#             return " ".join([seg.text for seg in segments]).strip()
#         except Exception as e:
#             print(f"[STT][Faster Whisper] Error: {e}")
#             return ""




# import numpy as np
# import whisper
# from modules.stt.faster_whisper_stt import WhisperModel
#
#
# # -----------------------------
# # Hybrid STT (Whisper + Faster Whisper)
# # -----------------------------
#
# class HybridSTT:
#     def __init__(self, whisper_model="small", fw_model="small", use_gpu=False, samplerate=16000):
#         self.samplerate = samplerate
#         self.use_gpu = use_gpu
#
#         # Whisper for short commands
#         device = "cuda" if use_gpu else "cpu"
#         print(f"[HybridSTT] Loading Whisper ({whisper_model}) on {device}...")
#         self.whisper_model = whisper.load_model(whisper_model, device=device)
#
#         # Faster Whisper (int8) for long dictation
#         print(f"[HybridSTT] Loading Faster Whisper ({fw_model}) on {device}...")
#         self.fw_model = WhisperModel(fw_model, device=device, compute_type="int8")
#
#     def transcribe(self, audio_array, long=False):
#         """Transcribe audio using Whisper (short) or Faster Whisper (long)."""
#         if audio_array.ndim > 1:
#             audio_array = audio_array.mean(axis=1)  # mono
#
#         audio_float = audio_array.astype(np.float32) / 32768.0
#
#         if not long:
#             # Whisper CPU for short commands
#             duration_sec = len(audio_array) / self.samplerate
#             # split into small slices if longer than 2s to prevent memory spikes
#             chunk_size = 2 * self.samplerate
#             text = ""
#             for i in range(0, len(audio_array), chunk_size):
#                 chunk = audio_array[i:i+chunk_size].astype(np.float32) / 32768.0
#                 try:
#                     result = self.whisper_model.transcribe(chunk, language="en")
#                     text += result.get("text", "") + " "
#                 except Exception as e:
#                     print(f"[Whisper] Error: {e}")
#             return text.strip()
#         else:
#             # Faster Whisper for long dictation
#             try:
#                 segments, _ = self.fw_model.transcribe(
#                     audio_float,
#                     language="en",
#                     temperature=0.0,
#                     suppress_blank=True,
#                     word_timestamps=False,
#                     beam_size=1
#                 )
#                 return " ".join([seg.text for seg in segments]).strip()
#             except Exception as e:
#                 print(f"[Faster Whisper] Error: {e}")
#                 return ""








# import os
# import numpy as np
# import sounddevice as sd
# from scipy.io.wavfile import write
# import whisper
# from faster_whisper import WhisperModel
#
#
# class HybridSTT:
#     def __init__(self, fw_model="small", whisper_model="small", use_gpu=False, samplerate=16000):
#         """
#         Hybrid STT:
#         - Short audio → Faster Whisper (int8) for fast commands
#         - Long audio  → Whisper CPU for long dictation
#         """
#         self.samplerate = samplerate
#         self.use_gpu = use_gpu
#
#         # Faster Whisper (int8) for short commands
#         device_fw = "cuda" if use_gpu else "cpu"
#         self.fw_model = WhisperModel(
#             fw_model, device=device_fw, compute_type="int8"
#         )
#
#         # Whisper CPU for long dictation
#         device_whisper = "cuda" if use_gpu else "cpu"
#         print(f"[STT] Loading Whisper model '{whisper_model}' on {device_whisper}...")
#         self.whisper_model = whisper.load_model(whisper_model, device=device_whisper)
#         print("[STT] Whisper model loaded.")
#
#     def transcribe(self, audio_array):
#         duration_sec = len(audio_array) / self.samplerate
#
#         # Convert to mono float32
#         if audio_array.ndim > 1:
#             audio_array = audio_array.mean(axis=1)
#         audio_float = audio_array.astype(np.float32) / 32768.0
#
#         if duration_sec <= 5.0:
#             # Short audio → Faster Whisper
#             segments, _ = self.fw_model.transcribe(
#                 audio_float,
#                 language="en",
#                 temperature=0.0,
#                 suppress_blank=True,
#                 word_timestamps=False,
#                 beam_size=1
#             )
#             text = " ".join([seg.text for seg in segments]).strip()
#             # Save to capture.wav for record
#             write("capture.wav", self.samplerate, audio_array)
#             return text
#         else:
#             # Long audio → Whisper CPU
#             # Save to temp file
#             filename = "capture.wav"
#             write(filename, self.samplerate, audio_array)
#             try:
#                 result = self.whisper_model.transcribe(filename, language="en")
#                 return result.get("text", "").strip()
#             except Exception as e:
#                 print(f"[Whisper] Error: {e}")
#                 return ""






# class HybridSTT:
#     def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
#         self.use_gpu = use_gpu
#         self.samplerate = 16000
#
#         # Whisper CPU for short commands
#         device = "cuda" if use_gpu else "cpu"
#         self.whisper_model = whisper.load_model(whisper_model, device=device)
#
#         # Faster Whisper int8 for long dictation
#         self.fw_model = WhisperModel(fw_model, device=device, compute_type="int8")
#
#     def transcribe(self, audio_array, long=False):
#         """Transcribe audio; use Whisper for short commands, Faster Whisper for long dictation."""
#         if long:
#             # Long dictation → Faster Whisper
#             if audio_array.ndim > 1:
#                 audio_array = audio_array.mean(axis=1)
#             audio_float = audio_array.astype(np.float32) / 32768.0
#             segments, _ = self.fw_model.transcribe(
#                 audio_float,
#                 language="en",
#                 temperature=0.0,
#                 suppress_blank=True,
#                 word_timestamps=False,
#                 beam_size=1,
#                 max_new_tokens=300  # <-- limit hallucination
#             )
#             return " ".join([seg.text for seg in segments]).strip()
#         else:
#             # Short command → Whisper
#             audio_float = audio_array.astype(np.float32) / 32768.0
#             try:
#                 result = self.whisper_model.transcribe(audio_float, language="en")
#                 return result.get("text", "").strip()
#             except Exception as e:
#                 print(f"[Whisper] Error: {e}")
#                 return ""
#
#
#
#
#
#
# import os
# import subprocess
# import shlex
# import sounddevice as sd
# import numpy as np
# import simpleaudio as sa
# import yaml
# import whisper
# from modules.stt.faster_whisper_stt import WhisperModel
# from TTS.api import TTS


# -----------------------------
# Hybrid STT (Whisper + Faster Whisper)
# -----------------------------
#
# import whisper
# from faster_whisper import WhisperModel
# import sounddevice as sd
# import numpy as np
# from scipy.io.wavfile import write
#
# class HybridSTT:
#     def __init__(self, whisper_model="small", fw_model="small", use_gpu=False, samplerate=16000):
#         self.use_gpu = use_gpu
#         self.samplerate = samplerate
#         self.temp_file = "capture.wav"
#
#         # Whisper CPU for short commands
#         print("[HybridSTT] Loading Whisper CPU model...")
#         self.whisper_model = whisper.load_model(whisper_model, device="cpu")
#         print("[HybridSTT] Whisper loaded.")
#
#         # Faster Whisper CPU for long dictation
#         device = "cuda" if use_gpu else "cpu"
#         self.fw_model = WhisperModel(fw_model, device=device, compute_type="int8")
#         print("[HybridSTT] Faster Whisper loaded.")
#
#     def record(self, duration=5):
#         print("[HybridSTT] Listening... Speak now.")
#         audio = sd.rec(int(duration * self.samplerate), samplerate=self.samplerate, channels=1, dtype="int16")
#         sd.wait()
#         write(self.temp_file, self.samplerate, audio)
#         return audio
#
#     def transcribe(self, audio_array):
#         if audio_array.ndim > 1:
#             audio_array = audio_array.mean(axis=1)
#
#         duration_sec = len(audio_array) / self.samplerate
#
#         if duration_sec <= 3.0:
#             # Short command → Whisper CPU safe via file
#             write(self.temp_file, self.samplerate, audio_array)
#             try:
#                 result = self.whisper_model.transcribe(self.temp_file, language="en")
#                 return result.get("text", "").strip()
#             except Exception as e:
#                 print(f"[Whisper] Error: {e}")
#                 return ""
#         else:
#             # Long dictation → Faster Whisper int8
#             audio_float = audio_array.astype(np.float32) / 32768.0
#             segments, _ = self.fw_model.transcribe(
#                 audio_float,
#                 language="en",
#                 temperature=0.0,
#                 suppress_blank=True,
#                 word_timestamps=False,
#                 beam_size=1
#             )
#             return " ".join([seg.text for seg in segments]).strip()


















# class HybridSTT:
#     def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
#         self.use_gpu = use_gpu
#         self.samplerate = 16000
#
#         # Whisper (CPU) for short commands
#         self.whisper_model = whisper.load_model(
#             whisper_model, device="cuda" if use_gpu else "cpu"
#         )
#
#         # Faster Whisper (int8) for long audio
#         device = "cuda" if use_gpu else "cpu"
#         self.fw_model = WhisperModel(
#             fw_model, device=device, compute_type="int8"
#         )
#
#     def transcribe(self, audio_array):
#         duration_sec = len(audio_array) / self.samplerate
#
#         if duration_sec <= 3:
#             # Short command → Whisper CPU
#             # Split into small slices to avoid memory spike
#             chunk_size = 2 * self.samplerate  # 2s
#             result_text = ""
#             for i in range(0, len(audio_array), chunk_size):
#                 chunk = audio_array[i:i + chunk_size]
#                 audio_float = chunk.astype(np.float32) / 32768.0
#                 try:
#                     result = self.whisper_model.transcribe(audio_float, language="en")
#                     result_text += result["text"] + " "
#                 except Exception as e:
#                     print(f"[Whisper] Error: {e}")
#             return result_text.strip()
#         else:
#             # Long dictation → Faster Whisper
#             if audio_array.ndim > 1:
#                 audio_array = audio_array.mean(axis=1)
#             audio_float = audio_array.astype(np.float32) / 32768.0
#             segments, _ = self.fw_model.transcribe(
#                 audio_float,
#                 language="en",
#                 temperature=0.0,
#                 suppress_blank=True,
#                 word_timestamps=False,
#                 beam_size=1
#             )
#             return " ".join([seg.text for seg in segments]).strip()
#



































# class HybridSTT:
#     def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
#         # Whisper for short commands
#         self.whisper_model = whisper.load_model(whisper_model, device="cuda" if use_gpu else "cpu")
#         # Faster Whisper for long audio
#         device = "cuda" if use_gpu else "cpu"
#         self.fw_model = WhisperModel(fw_model, device=device, compute_type="int8")
#         self.samplerate = 16000
#
#     def transcribe(self, audio_array):
#         duration_sec = len(audio_array) / self.samplerate
#
#         if duration_sec < 3:
#             # Short commands → Whisper
#             audio_float = audio_array.astype(np.float32) / 32768.0
#             result = self.whisper_model.transcribe(audio_float, language="en")
#             return result["text"].strip()
#         else:
#             # Long dictation → Faster Whisper
#             if audio_array.ndim > 1:
#                 audio_array = audio_array.mean(axis=1)
#             audio_float = audio_array.astype(np.float32) / 32768.0
#             segments, _ = self.fw_model.transcribe(
#                 audio_float,
#                 language="en",
#                 temperature=0.0,
#                 suppress_blank=True,
#                 word_timestamps=False,
#                 beam_size=1,
#             )
#             return " ".join([seg.text for seg in segments]).strip()





    # def __init__(self, whisper_model="small", fw_model="small", use_gpu=False):
    #     # Whisper for short commands
    #     self.whisper_model = whisper.load_model(whisper_model, device="cuda" if use_gpu else "cpu")
    #
    #     # Faster Whisper for long audio
    #     device = "cuda" if use_gpu else "cpu"
    #     self.fw_model = WhisperModel(fw_model, device=device, compute_type="int8")
    #
    #     self.samplerate = 16000
    #
    # def transcribe(self, audio_array):
    #     duration_sec = len(audio_array) / self.samplerate
    #
    #     if duration_sec < 3:
    #         # Short command → Whisper
    #         audio_float = audio_array.astype(np.float32) / 32768.0
    #         result = self.whisper_model.transcribe(audio_float, language="en")
    #         return result["text"]
    #     else:
    #         # Long dictation → Faster Whisper
    #         if audio_array.ndim > 1:
    #             audio_array = audio_array.mean(axis=1)
    #         audio_float = audio_array.astype(np.float32) / 32768.0
    #         segments, _ = self.fw_model.transcribe(
    #             audio_float,
    #             language="en",
    #             temperature=0.0,
    #             suppress_blank=True,
    #             word_timestamps=False,
    #             beam_size=1,
    #         )
    #         return " ".join([seg.text for seg in segments])
