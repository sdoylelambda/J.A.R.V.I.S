import pytest
import numpy as np
from unittest.mock import MagicMock, patch


def make_audio_bytes(rms: float = 3000, duration_seconds: float = 1.0, rate: int = 16000) -> bytes:
    n_samples = int(rate * duration_seconds)
    amplitude = min(int(rms * np.sqrt(2)), 32767)
    samples = np.full(n_samples, amplitude, dtype=np.int16)
    return samples.tobytes()


# ─────────────────────────────────────────────
# HybridSTT — float32 conversion
# ─────────────────────────────────────────────

class TestHybridSTTConversion:
    def _make_stt(self):
        with patch("whisper.load_model"), patch("faster_whisper.WhisperModel"):
            from modules.stt.hybrid_stt import HybridSTT
            stt = HybridSTT(whisper_model="tiny", fw_model="tiny")
        stt._transcribe_short = MagicMock(return_value="short result")
        stt._transcribe_long = MagicMock(return_value="long result")
        return stt

    def test_to_float32_normalizes_range(self):
        stt = self._make_stt()
        audio_bytes = make_audio_bytes(rms=10000)
        result = stt._to_float32(audio_bytes)
        assert result.dtype == np.float32
        assert result.max() <= 1.0
        assert result.min() >= -1.0

    def test_to_float32_silent_audio(self):
        stt = self._make_stt()
        silent = np.zeros(1024, dtype=np.int16).tobytes()
        result = stt._to_float32(silent)
        assert np.all(result == 0.0)

    def test_to_float32_returns_numpy_array(self):
        stt = self._make_stt()
        audio_bytes = make_audio_bytes()
        result = stt._to_float32(audio_bytes)
        assert isinstance(result, np.ndarray)


# ─────────────────────────────────────────────
# HybridSTT — routing
# ─────────────────────────────────────────────

class TestHybridSTTRouting:
    def _make_stt(self):
        with patch("whisper.load_model"), patch("faster_whisper.WhisperModel"):
            from modules.stt.hybrid_stt import HybridSTT
            stt = HybridSTT(whisper_model="tiny", fw_model="tiny")
            stt._transcribe_short = MagicMock(return_value="short result")
            stt._transcribe_long = MagicMock(return_value="long result")
            return stt

    def test_short_audio_uses_faster_whisper(self):
        stt = self._make_stt()
        audio_bytes = make_audio_bytes(duration_seconds=1.0)
        with patch.object(stt, "_transcribe_short", return_value="short result") as mock_short:
            stt.transcribe(audio_bytes, duration=1.0)
        mock_short.assert_called_once()

    def test_long_audio_uses_whisper(self):
        stt = self._make_stt()
        audio_bytes = make_audio_bytes(duration_seconds=15.0)
        with patch.object(stt, "_transcribe_long", return_value="long result") as mock_long:
            stt.transcribe(audio_bytes, duration=15.0)
        mock_long.assert_called_once()

    def test_returns_short_result(self):
        stt = self._make_stt()
        audio_bytes = make_audio_bytes(duration_seconds=1.0)
        result = stt.transcribe(audio_bytes, duration=1.0)
        assert result == "short result"

    def test_returns_long_result(self):
        stt = self._make_stt()
        audio_bytes = make_audio_bytes(duration_seconds=15.0)
        result = stt.transcribe(audio_bytes, duration=15.0)
        assert result == "long result"

    def test_too_short_audio_returns_empty(self):
        with patch("whisper.load_model"), patch("faster_whisper.WhisperModel"):
            from modules.stt.hybrid_stt import HybridSTT
            stt = HybridSTT(whisper_model="tiny", fw_model="tiny")

        # Audio shorter than 0.5s minimum
        tiny_audio = make_audio_bytes(duration_seconds=0.1)
        result = stt.transcribe(tiny_audio, duration=0.1)
        assert result == ""
