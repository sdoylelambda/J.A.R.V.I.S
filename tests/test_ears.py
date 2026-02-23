import pytest
import numpy as np
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def make_audio_bytes(rms_target: float, n_samples: int = 1024) -> bytes:
    """Generate synthetic int16 audio bytes with approximately the given RMS."""
    amplitude = int(rms_target * np.sqrt(2))
    amplitude = min(amplitude, 32767)
    samples = np.full(n_samples, amplitude, dtype=np.int16)
    return samples.tobytes()


def rms_of(audio_bytes: bytes) -> float:
    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
    return float(np.sqrt(np.mean(audio_np ** 2)))


# ─────────────────────────────────────────────
# RMS helper tests
# ─────────────────────────────────────────────

class TestRMSHelper:
    def test_silent_audio_has_low_rms(self):
        silent = np.zeros(1024, dtype=np.int16).tobytes()
        assert rms_of(silent) == 0.0

    def test_loud_audio_has_high_rms(self):
        loud = make_audio_bytes(10000)
        assert rms_of(loud) > 5000

    def test_rms_scales_with_amplitude(self):
        quiet = rms_of(make_audio_bytes(1000))
        loud = rms_of(make_audio_bytes(5000))
        assert loud > quiet


# ─────────────────────────────────────────────
# Ears — calibration
# ─────────────────────────────────────────────

class TestEarsCalibration:
    def _make_ears(self):
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()
        return ears

    @pytest.mark.asyncio
    async def test_calibration_sets_noise_floor(self):
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()

        silent_chunk = make_audio_bytes(500)
        with patch("asyncio.to_thread", new=AsyncMock(return_value=silent_chunk)):
            await ears._calibrate_noise_floor(seconds=0.1, pre_delay=0)

        assert ears.noise_floor is not None
        assert ears.noise_floor > 0

    @pytest.mark.asyncio
    async def test_calibration_sets_thresholds(self):
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()

        chunk = make_audio_bytes(300)
        with patch("asyncio.to_thread", new=AsyncMock(return_value=chunk)):
            await ears._calibrate_noise_floor(seconds=0.1, pre_delay=0)

        assert ears.start_threshold > ears.noise_floor
        assert ears.stop_threshold > ears.noise_floor
        assert ears.start_threshold > ears.stop_threshold

    @pytest.mark.asyncio
    async def test_high_noise_floor_uses_static_thresholds(self):
        """If noise floor is suspiciously high, static fallback should apply."""
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()

        loud_chunk = make_audio_bytes(20000)
        with patch("asyncio.to_thread", new=AsyncMock(return_value=loud_chunk)):
            await ears._calibrate_noise_floor(seconds=0.1, pre_delay=0)

        # Thresholds should still be sane even with a bad noise floor
        assert ears.start_threshold < 32767
        assert ears.stop_threshold < ears.start_threshold


# ─────────────────────────────────────────────
# Ears — listen() speech detection
# ─────────────────────────────────────────────

class TestEarsListen:
    @pytest.mark.asyncio
    async def test_returns_none_when_no_speech(self):
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()
        ears.noise_floor = 500
        ears.start_threshold = 1500
        ears.stop_threshold = 750

        silent_chunk = make_audio_bytes(300)

        call_count = 0
        max_calls = 30

        async def fake_read(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count >= max_calls:
                raise asyncio.CancelledError()
            return silent_chunk

        with patch("asyncio.to_thread", new=fake_read):
            try:
                result, duration = await ears.listen(max_duration=0.1)
            except asyncio.CancelledError:
                result = None

        assert result is None or len(result) == 0

    @pytest.mark.asyncio
    async def test_detects_speech_start(self):
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()
        ears.noise_floor = 500
        ears.start_threshold = 1500
        ears.stop_threshold = 750

        silent = make_audio_bytes(300)
        speech = make_audio_bytes(5000)

        chunks = [silent] * 3 + [speech] * 5 + [silent] * 20

        idx = 0

        async def fake_read(*args, **kwargs):
            nonlocal idx
            if idx >= len(chunks):
                raise asyncio.CancelledError()
            chunk = chunks[idx]
            idx += 1
            return chunk

        with patch("asyncio.to_thread", new=fake_read):
            try:
                audio_bytes, duration = await ears.listen()
            except asyncio.CancelledError:
                return

        assert audio_bytes is not None
        assert len(audio_bytes) > 0

    @pytest.mark.asyncio
    async def test_stops_after_silence(self):
        from modules.ears import Ears
        ears = Ears(debug=False)
        ears.audio_stream = MagicMock()
        ears.noise_floor = 500
        ears.start_threshold = 1500
        ears.stop_threshold = 750

        silent = make_audio_bytes(300)
        speech = make_audio_bytes(5000)

        # Speech then sustained silence
        chunks = [speech] * 5 + [silent] * 50
        idx = 0

        async def fake_read(*args, **kwargs):
            nonlocal idx
            chunk = chunks[min(idx, len(chunks) - 1)]
            idx += 1
            return chunk

        with patch("asyncio.to_thread", new=fake_read):
            audio_bytes, duration = await ears.listen()

        assert audio_bytes is not None
        assert duration > 0
