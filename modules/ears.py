# modules/ears.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

class Ears:
    def __init__(self, samplerate=16000, mic_index=None, duration=7):
        self.samplerate = samplerate
        self.mic_index = mic_index
        self.duration = duration

    def _has_speech(self, audio, threshold=0.01):
        rms = np.sqrt(np.mean(audio ** 2))
        return rms > threshold

    def listen(self, filename="capture.wav"):
        print("[Ears] Listening... Please speak now.")

        audio = sd.rec(
            int(self.duration * self.samplerate),
            samplerate=self.samplerate,
            channels=1,
            dtype="int16",
            device=self.mic_index
        )
        sd.wait()

        audio = audio.flatten().astype(np.float32) / 32768.0

        if not self._has_speech(audio):
            print("[Ears] Silence detected. Ignoring.")
            return None, 0.0

        write(filename, self.samplerate, (audio * 32768).astype(np.int16))
        return filename, len(audio) / self.samplerate









# # modules/ears.py
# import sounddevice as sd
# import numpy as np
# from scipy.io.wavfile import write
#
# class Ears:
#     def __init__(self, stt, samplerate=16000, mic_index=None, duration=7, short_threshold=5.0):
#         """
#         stt: HybridSTT instance
#         samplerate: recording sample rate
#         mic_index: optional device index
#         duration: max recording duration for capture.wav
#         short_threshold: max seconds considered a 'short command'
#         """
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#         self.duration = duration
#         self.short_threshold = short_threshold
#
#     def listen(self, duration=None, filename="capture.wav"):
#         duration = duration or self.duration
#         print("[Ears] Listening... Please speak now.")
#
#         audio = sd.rec(
#             int(duration * self.samplerate),
#             samplerate=self.samplerate,
#             channels=1,
#             dtype="int16",
#             device=self.mic_index
#         )
#         sd.wait()
#
#         audio = audio.flatten().astype(np.float32) / 32768.0
#
#         def has_speech(audio, threshold=0.01):
#             rms = np.sqrt(np.mean(audio.astype(np.float32) ** 2))
#             return rms > threshold
#
#         # 🔴 SILENCE GUARD
#         if not has_speech(audio):
#             print("[Ears] No speech detected. Ignoring.")
#             return None
#
#         write(filename, self.samplerate, (audio * 32768).astype(np.int16))
#         return filename
#
#     def listen_stream(self, audio_array=None, chunk_sec=1.0):
#         """
#         Streaming generator for long dictation only.
#         Yields partial transcription every chunk_sec seconds.
#         """
#         if audio_array is None:
#             print("[Ears] Recording long dictation for streaming...")
#             audio_array = sd.rec(int(self.duration * self.samplerate),
#                                  samplerate=self.samplerate,
#                                  channels=1,
#                                  dtype="int16",
#                                  device=self.mic_index)
#             sd.wait()
#
#         buffer = np.zeros((0,), dtype=np.int16)
#         chunk_samples = int(chunk_sec * self.samplerate)
#
#         for start in range(0, len(audio_array), chunk_samples):
#             chunk = audio_array[start:start+chunk_samples].flatten()
#             buffer = np.concatenate((buffer, chunk))
#
#             if len(buffer) >= chunk_samples:
#                 audio_float = buffer.astype(np.float32) / 32768.0
#                 text = self.stt.transcribe_long(audio_float)
#                 if text:
#                     yield text
#                 buffer = np.zeros((0,), dtype=np.int16)








# modules/ears.py
# import sounddevice as sd
# import numpy as np
# from scipy.io.wavfile import write
#
# class Ears:
#     def __init__(self, stt, samplerate=16000, mic_index=None, duration=7):
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#         self.duration = duration  # max recording duration
#
#     def listen(self, filename="capture.wav"):
#         """Record full audio to capture.wav"""
#         print("[Ears] Listening... Please speak now.")
#         audio = sd.rec(int(self.duration * self.samplerate),
#                        samplerate=self.samplerate,
#                        channels=1,
#                        dtype="int16",
#                        device=self.mic_index)
#         sd.wait()
#         write(filename, self.samplerate, audio)
#
#         # Decide which STT to use based on duration
#         duration_sec = len(audio) / self.samplerate
#         if duration_sec <= 5.0:
#             # Short command
#             text = self.stt.transcribe_short(filename)
#         else:
#             # Long dictation
#             text = self.stt.transcribe_long(audio)
#         return text





# import numpy as np
# import sounddevice as sd
#
#
# class Ears:
#     def __init__(self, stt, samplerate=16000, mic_index=None, duration=7):
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#         self.max_duration = duration  # max recording length
#         self.short_chunk_sec = 1.0
#         self.long_chunk_sec = 5.0
#
#     def listen(self):
#         """Record audio and return transcription (short/long auto-detect)."""
#         print(f"[Ears] Listening for up to {self.max_duration}s...")
#         audio = sd.rec(int(self.max_duration * self.samplerate),
#                        samplerate=self.samplerate,
#                        channels=1,
#                        dtype='int16',
#                        device=self.mic_index)
#         sd.wait()
#         duration_sec = len(audio) / self.samplerate
#
#         if duration_sec <= 5.0:
#             return self.stt.transcribe(audio, long=False)
#         else:
#             return self.stt.transcribe(audio, long=True)
#
#     def listen_stream(self, short_chunk_sec=1.0, long_chunk_sec=5.0):
#         """Yield transcribed text continuously."""
#         self.short_chunk_sec = short_chunk_sec
#         self.long_chunk_sec = long_chunk_sec
#
#         short_buffer = np.zeros((0,), dtype=np.int16)
#         long_buffer = np.zeros((0,), dtype=np.int16)
#
#         try:
#             with sd.InputStream(
#                 samplerate=self.samplerate,
#                 channels=1,
#                 dtype="int16",
#                 device=self.mic_index,
#                 blocksize=int(self.samplerate * self.short_chunk_sec)
#             ) as stream:
#                 print("[Ears] Streaming started...")
#                 while True:
#                     chunk, _ = stream.read(int(self.samplerate * self.short_chunk_sec))
#                     chunk = chunk.flatten()
#                     short_buffer = np.concatenate((short_buffer, chunk))
#                     long_buffer = np.concatenate((long_buffer, chunk))
#
#                     # Process short buffer
#                     if len(short_buffer) >= int(self.short_chunk_sec * self.samplerate):
#                         text = self.stt.transcribe(short_buffer, long=False)
#                         if text:
#                             yield text
#                         short_buffer = np.zeros((0,), dtype=np.int16)
#
#                     # Process long buffer
#                     if len(long_buffer) >= int(self.long_chunk_sec * self.samplerate):
#                         text = self.stt.transcribe(long_buffer, long=True)
#                         if text:
#                             yield text
#                         long_buffer = np.zeros((0,), dtype=np.int16)
#
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")
#         except Exception as e:
#             print(f"[Ears] Error: {e}")
#
#











# modules/ears.py
# import numpy as np
# import sounddevice as sd
#
# class Ears:
#     def __init__(self, stt, samplerate=16000, mic_index=None, duration=7):
#         """
#         Streaming microphone listener with short and long buffers.
#         - stt: HybridSTT instance
#         - samplerate: microphone sample rate
#         - mic_index: optional mic index
#         - duration: max recording length for long buffer
#         """
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#         self.duration = duration  # max buffer for long dictation in seconds
#
#         # Buffers
#         self.short_buffer = np.zeros((0,), dtype=np.int16)
#         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#         # Short/long chunk sizes
#         self.short_chunk_sec = 1.0   # Whisper short commands
#         self.long_chunk_sec = 5.0    # Faster Whisper long dictation
#
#     def listen_stream(self):
#         """Continuously read from mic and yield transcribed text for short and long audio."""
#         print("[Ears] Starting streaming...")
#
#         try:
#             with sd.InputStream(
#                 samplerate=self.samplerate,
#                 channels=1,
#                 dtype="int16",
#                 device=self.mic_index,
#                 blocksize=int(self.samplerate * 0.25)  # 250ms blocks for responsiveness
#             ) as stream:
#
#                 while True:
#                     # Read a block
#                     chunk, _ = stream.read(int(self.samplerate * 0.25))
#                     chunk = chunk.flatten()
#
#                     # Append to buffers
#                     self.short_buffer = np.concatenate((self.short_buffer, chunk))
#                     self.long_buffer = np.concatenate((self.long_buffer, chunk))
#
#                     # Process short buffer
#                     if len(self.short_buffer) >= int(self.short_chunk_sec * self.samplerate):
#                         audio_short = self.short_buffer[:int(self.short_chunk_sec * self.samplerate)]
#                         text = self.stt.transcribe(audio_short)
#                         if text:
#                             yield text
#                         self.short_buffer = np.zeros((0,), dtype=np.int16)
#
#                     # Process long buffer
#                     if len(self.long_buffer) >= int(self.long_chunk_sec * self.samplerate):
#                         audio_long = self.long_buffer[:int(self.long_chunk_sec * self.samplerate)]
#                         text = self.stt.transcribe(audio_long)
#                         if text:
#                             yield text
#                         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")
#         except Exception as e:
#             print(f"[Ears] Error: {e}")














# ears.py
# import numpy as np
# import sounddevice as sd
# from scipy.io.wavfile import write
#
#
# class Ears:
#     def __init__(self, stt, samplerate=16000, mic_index=0, duration=7):
#         """
#         Streaming microphone wrapper.
#         - stt: HybridSTT instance
#         - samplerate: recording sample rate
#         - mic_index: microphone device index
#         - duration: maximum buffer length for long dictation
#         """
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#         self.duration = duration
#
#         # Buffers for streaming
#         self.short_buffer = np.zeros((0,), dtype=np.int16)
#         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#     def listen(self, duration=None, filename="capture.wav"):
#         """
#         Record a single slice and transcribe immediately (for short commands).
#         """
#         duration = duration or self.duration
#         print("[Ears] Listening... Please speak now.")
#         audio = sd.rec(int(duration * self.samplerate),
#                        samplerate=self.samplerate,
#                        channels=1,
#                        dtype='int16',
#                        device=self.mic_index)
#         sd.wait()
#         write(filename, self.samplerate, audio)
#
#         audio_array = audio.flatten()
#         return self.stt.transcribe(audio_array, long=(duration > 5.0))
#
#     def listen_stream(self, short_chunk_sec=1.0, long_chunk_sec=5.0):
#         """
#         Streaming input from mic.
#         - short_chunk_sec: duration of short buffer (Whisper)
#         - long_chunk_sec: duration of long buffer (Faster Whisper)
#         Yields transcribed text chunks.
#         """
#         print("[Ears] Starting overlapping streaming...")
#         short_chunk_samples = int(short_chunk_sec * self.samplerate)
#         long_chunk_samples = int(long_chunk_sec * self.samplerate)
#
#         try:
#             with sd.InputStream(
#                 samplerate=self.samplerate,
#                 channels=1,
#                 dtype="int16",
#                 device=self.mic_index,
#                 blocksize=short_chunk_samples
#             ) as stream:
#
#                 while True:
#                     chunk, _ = stream.read(short_chunk_samples)
#                     chunk = chunk.flatten()
#
#                     # Append to buffers
#                     self.short_buffer = np.concatenate((self.short_buffer, chunk))
#                     self.long_buffer = np.concatenate((self.long_buffer, chunk))
#
#                     # Process short buffer
#                     if len(self.short_buffer) >= short_chunk_samples:
#                         audio_float = self.short_buffer.astype(np.float32) / 32768.0
#                         try:
#                             text = self.stt.transcribe(audio_float, long=False)
#                             if text:
#                                 yield text
#                         except Exception as e:
#                             print(f"[Ears][Short] STT error: {e}")
#                         self.short_buffer = np.zeros((0,), dtype=np.int16)
#
#                     # Process long buffer
#                     if len(self.long_buffer) >= long_chunk_samples:
#                         audio_float = self.long_buffer.astype(np.float32) / 32768.0
#                         try:
#                             text = self.stt.transcribe(audio_float, long=True)
#                             if text:
#                                 yield text
#                         except Exception as e:
#                             print(f"[Ears][Long] STT error: {e}")
#                         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")
#         except Exception as e:
#             print(f"[Ears] Error: {e}")
#









# import sounddevice as sd
# import numpy as np
#
#
# class Ears:
#     def __init__(self, stt, mic_index=0, duration=5, samplerate=16000, use_mock=False):
#         self.stt = stt
#         self.mic_index = mic_index
#         self.duration = duration
#         self.samplerate = samplerate
#         self.use_mock = use_mock
#
#     def listen(self, duration=None):
#         """Record audio and return transcription."""
#         if self.use_mock:
#             return input("Simulated audio: ")
#
#         duration = duration or self.duration
#         print("[Ears] Listening... Please speak now.")
#         audio = sd.rec(
#             int(duration * self.samplerate),
#             samplerate=self.samplerate,
#             channels=1,
#             dtype="int16",
#             device=self.mic_index
#         )
#         sd.wait()
#         print("[Ears] Processing transcription...")
#         return self.stt.transcribe(audio)


















# class Ears:
#     """
#     Continuous audio capture with overlapping short/long buffers.
#     Short: ≤1s → Whisper CPU for commands.
#     Long: ≥3s → Faster Whisper for dictation.
#     """
#     def __init__(self, stt, samplerate=16000, mic_index=None):
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#
#         self.short_buffer = np.zeros((0,), dtype=np.int16)
#         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#         self.short_chunk_sec = 0.5  # process every 0.5s for short commands
#         self.long_chunk_sec = 3.0   # process every 3s for long dictation
#
#     def listen_stream(self):
#         """
#         Generator that yields transcribed text in short and long chunks.
#         Uses internal buffers for short and long speech detection.
#         """
#         print("[Ears] Starting overlapping streaming...")
#         self.short_buffer = np.zeros((0,), dtype=np.int16)
#         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#         try:
#             with sd.InputStream(
#                     samplerate=self.samplerate,  # <- correct
#                     channels=1,
#                     dtype="int16",
#                     device=self.mic_index,
#                     blocksize=int(self.samplerate * self.short_chunk_sec)  # samples per read
#             ) as stream:
#
#                 while True:
#                     chunk, _ = stream.read(int(self.samplerate * self.short_chunk_sec))
#                     chunk = chunk.flatten()
#
#                     # Append to both buffers
#                     self.short_buffer = np.concatenate((self.short_buffer, chunk))
#                     self.long_buffer = np.concatenate((self.long_buffer, chunk))
#
#                     # Process short buffer
#                     if len(self.short_buffer) >= int(self.short_chunk_sec * self.samplerate):
#                         audio_float = self.short_buffer.astype(np.float32) / 32768.0
#                         try:
#                             text = self.stt.transcribe(audio_float, short=True)
#                             if text:
#                                 yield text
#                         except Exception as e:
#                             print(f"[Ears][Short] STT error: {e}")
#                         self.short_buffer = np.zeros((0,), dtype=np.int16)
#
#                     # Process long buffer
#                     if len(self.long_buffer) >= int(self.long_chunk_sec * self.samplerate):
#                         audio_float = self.long_buffer.astype(np.float32) / 32768.0
#                         try:
#                             text = self.stt.transcribe(audio_float, short=False)
#                             if text:
#                                 yield text
#                         except Exception as e:
#                             print(f"[Ears][Long] STT error: {e}")
#                         self.long_buffer = np.zeros((0,), dtype=np.int16)
#
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")
#         except Exception as e:
#             print(f"[Ears] Error: {e}")










# class Ears:
#     """
#     Continuous audio capture from microphone, yielding chunks for STT.
#     Automatically splits audio into short (≤3s) and long (>3s) segments.
#     """
#     def __init__(self, stt, samplerate=16000, mic_index=None):
#         self.stt = stt
#         self.samplerate = samplerate
#         self.mic_index = mic_index
#         self.chunk_duration = 1.0  # 1 second chunk for streaming
#
#     def listen_stream(self):
#         """
#         Generator yielding transcribed text from live mic in near real-time.
#         """
#         print("[Ears] Starting continuous listening...")
#         buffer = np.zeros((0,), dtype=np.int16)
#
#         try:
#             with sd.InputStream(samplerate=self.samplerate,
#                                 channels=1,
#                                 dtype="int16",
#                                 device=self.mic_index,
#                                 blocksize=int(self.samplerate * self.chunk_duration)) as stream:
#
#                 while True:
#                     chunk, _ = stream.read(int(self.samplerate * self.chunk_duration))
#                     chunk = chunk.flatten()
#                     buffer = np.concatenate((buffer, chunk))
#
#                     duration_sec = len(buffer) / self.samplerate
#
#                     # Decide if it's short or long command
#                     if duration_sec >= 3.0:
#                         # Long command → Faster Whisper
#                         text = self.stt.transcribe(buffer)
#                         buffer = np.zeros((0,), dtype=np.int16)  # reset buffer
#                         if text:
#                             yield text
#                     elif duration_sec >= 0.5:
#                         # Short command → Whisper CPU (partial streaming)
#                         text = self.stt.transcribe(buffer)
#                         buffer = np.zeros((0,), dtype=np.int16)
#                         if text:
#                             yield text
#
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")
#         except Exception as e:
#             print(f"[Ears] Error: {e}")
#









# import sounddevice as sd
#
#
# class Ears:
#     def __init__(self, stt, mic_index=0, chunk_duration=1.5):
#         self.stt = stt
#         self.samplerate = stt.samplerate
#         self.chunk_duration = chunk_duration
#         self.mic_index = mic_index
#
#     def listen_stream(self):
#         """Yields transcribed text chunk-by-chunk."""
#         print("[Ears] Listening... Speak now.")
#         try:
#             while True:
#                 audio = sd.rec(
#                     int(self.chunk_duration * self.samplerate),
#                     samplerate=self.samplerate,
#                     channels=1,
#                     dtype="int16",
#                     device=self.mic_index
#                 )
#                 sd.wait()
#                 text = self.stt.transcribe(audio)
#                 if text:
#                     yield text
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")



















# class Ears:
#     def __init__(self, stt, mic_index=0, chunk_duration=1.5):
#         self.stt = stt
#         self.samplerate = stt.samplerate
#         self.chunk_duration = chunk_duration
#         self.mic_index = mic_index
#
#     def listen_stream(self):
#         """Yields transcribed text chunk-by-chunk."""
#         print("[Ears] Listening... Speak now.")
#         try:
#             while True:
#                 audio = sd.rec(
#                     int(self.chunk_duration * self.samplerate),
#                     samplerate=self.samplerate,
#                     channels=1,
#                     dtype="int16",
#                     device=self.mic_index
#                 )
#                 sd.wait()
#                 text = self.stt.transcribe(audio)
#                 if text:
#                     yield text
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")









# class Ears:
#     def __init__(self, stt, mic_index=0, chunk_duration=1.5):
#         """
#         chunk_duration: seconds per slice of audio to feed to STT
#         """
#         self.stt = stt
#         self.samplerate = stt.samplerate
#         self.chunk_duration = chunk_duration
#         self.mic_index = mic_index
#
#     def listen_stream(self):
#         """
#         Generator yielding transcribed text in near-real-time
#         """
#         print("[Ears] Listening... Speak now.")
#         try:
#             while True:
#                 audio = sd.rec(
#                     int(self.chunk_duration * self.samplerate),
#                     samplerate=self.samplerate,
#                     channels=1,
#                     dtype="int16",
#                     device=self.mic_index
#                 )
#                 sd.wait()
#                 text = self.stt.transcribe(audio).strip()
#                 if text:
#                     yield text
#         except KeyboardInterrupt:
#             print("[Ears] Stopped listening.")













# class Ears:
#     def __init__(self, stt, mic_index=0, duration=3):
#         self.stt = stt
#         self.samplerate = stt.samplerate
#         self.duration = duration
#         self.mic_index = mic_index
#
#     def listen(self):
#         print("[Ears] Listening... Please speak now.")
#         audio = sd.rec(
#             int(self.duration * self.samplerate),
#             samplerate=self.samplerate,
#             channels=1,
#             dtype="int16",
#             device=self.mic_index
#         )
#         sd.wait()
#         print("[Ears] Processing transcription...")
#         return self.stt.transcribe(audio)





# import sounddevice as sd
#
#
# class Ears:
#     def __init__(self, stt, use_mock=False):
#         self.stt = stt
#         self.samplerate = stt.samplerate
#         self.duration = stt.duration
#         self.mic_index = stt.mic_index
#         self.use_mock = use_mock
#
#     def listen(self, duration=None):
#         duration = duration or self.duration
#
#         if self.use_mock:
#             return input("Simulated audio: ")
#
#         print("[Ears] Listening... Please speak now.")
#         audio = sd.rec(
#             int(duration * self.samplerate),
#             samplerate=self.samplerate,
#             channels=1,
#             dtype="int16",
#             device=self.mic_index,
#         )
#         sd.wait()
#         print("[Ears] Processing transcription...")
#         return self.stt.transcribe(audio)
#
#
#







# import os
# import sounddevice as sd
# import numpy as np
# # import wavio  # for saving WAV files if needed
# from modules.stt.factory import create_stt  # assuming your factory is in stt/factory.py
# from scipy.io.wavfile import write
#
#
# class Ears:
#     """
#     Microphone interface for recording and transcribing audio.
#     Supports both Whisper and FasterWhisper via the STTFactory.
#     """
#
#     def __init__(self, stt, samplerate=16000, duration=5, mic_index=None, use_mock=False):        # STT engine
#         # self.stt = create_stt(config)
#         #
#         # # Audio settings
#         # self.samplerate = 16000
#         # self.duration = config["stt"]["duration"]
#         # self.mic_index = 0
#         # self.use_mock = use_mock
#         self.stt = stt
#         self.samplerate = samplerate
#         self.duration = duration
#         self.mic_index = mic_index
#         self.use_mock = use_mock
#
#     def listen(self, duration=None, filename="capture.wav"):
#         """
#         Record audio from the microphone and return transcribed text.
#         """
#         if self.use_mock:
#             return input("Simulated audio: ")
#
#         duration = duration or self.duration
#         print("[Ears] Listening... Please speak now.")
#
#         # Record audio
#         audio = sd.rec(
#             int(duration * self.samplerate),
#             samplerate=self.samplerate,
#             channels=1,
#             dtype="int16",
#             device=self.mic_index,
#         )
#         sd.wait()
#
#         # Save audio to WAV file (optional, useful for FasterWhisper)
#         # wavio.write(filename, audio, self.samplerate, sampwidth=2)
#         write(filename, self.samplerate, audio)
#
#         print("[Ears] Processing transcription...")
#         text = self.stt.transcribe(filename)
#         return text
#



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
