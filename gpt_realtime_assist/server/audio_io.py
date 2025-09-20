import sounddevice as sd
import numpy as np
from typing import Optional, Callable
from sounddevice import PortAudioError

class AudioIO:
    def __init__(self, sr: int, in_dev: Optional[str], out_dev: Optional[str]):
        self.sr = sr
        self.in_dev = None if in_dev in (None, "auto") else in_dev
        self.out_dev = None if out_dev in (None, "auto") else out_dev
        self._in = None
        self._out = None
        self._capture_warned = False
        self._playback_warned = False

        try:
            sd.default.samplerate = self.sr
        except Exception:
            pass

        if self.in_dev or self.out_dev:
            sd.default.device = (self.in_dev or None, self.out_dev or None)

    def list_devices(self):
        return sd.query_devices()

    def start_capture(self, on_frames: Callable[[bytes], None], block_ms: int = 20) -> bool:
        if self._in:
            return True
        frames = max(1, int(self.sr * block_ms / 1000))

        def cb(indata, frames, time, status):
            if status and not self._capture_warned:
                print("Audio input status:", status)
                self._capture_warned = True
            if indata.ndim == 1:
                pcm = (indata * 32767).astype(np.int16).tobytes()
            else:
                pcm = (indata[:, 0] * 32767).astype(np.int16).tobytes()
            on_frames(pcm)

        try:
            self._in = sd.InputStream(
                device=self.in_dev,
                channels=1,
                samplerate=self.sr,
                dtype="float32",
                callback=cb,
                blocksize=frames,
            )
            self._in.start()
            self._capture_warned = False
            return True
        except PortAudioError as err:
            if not self._capture_warned:
                dev = self.in_dev or "default"
                print(f"Failed to start capture on {dev}: {err}")
                self._capture_warned = True
            self._in = None
            return False

    def stop_capture(self):
        if self._in:
            try:
                self._in.stop()
                self._in.close()
            except PortAudioError as err:
                print("Error while stopping capture:", err)
            finally:
                self._in = None
                self._capture_warned = False

    def start_playback(self) -> bool:
        if self._out:
            return True
        try:
            self._out = sd.OutputStream(
                device=self.out_dev,
                channels=1,
                samplerate=self.sr,
                dtype="int16",
                blocksize=0,
            )
            self._out.start()
            self._playback_warned = False
            return True
        except PortAudioError as err:
            if not self._playback_warned:
                dev = self.out_dev or "default"
                print(f"Failed to open playback device {dev}: {err}")
                self._playback_warned = True
            self._out = None
            return False

    def play_bytes(self, pcm16: bytes):
        if not self._out:
            if not self.start_playback():
                return
        try:
            arr = np.frombuffer(pcm16, dtype=np.int16)
            self._out.write(arr)
        except PortAudioError as err:
            if not self._playback_warned:
                print("Playback error, resetting stream:", err)
                self._playback_warned = True
            self.stop_playback()

    def stop_playback(self):
        if self._out:
            try:
                self._out.stop()
                self._out.close()
            except PortAudioError as err:
                print("Error while stopping playback:", err)
            finally:
                self._out = None
                self._playback_warned = False
