import sounddevice as sd, numpy as np
from typing import Optional, Callable

class AudioIO:
    def __init__(self, sr:int, in_dev:Optional[str], out_dev:Optional[str]):
        self.sr=sr
        self.in_dev=None if in_dev in (None,"auto") else in_dev
        self.out_dev=None if out_dev in (None,"auto") else out_dev
        self._in=None; self._out=None

    def list_devices(self):
        return sd.query_devices()

    def start_capture(self, on_frames:Callable[[bytes],None], block_ms:int=20):
        frames=int(self.sr*block_ms/1000)
        def cb(indata, frames, time, status):
            if status: print("Audio in status:", status)
            if indata.ndim==1: pcm=(indata*32767).astype(np.int16).tobytes()
            else: pcm=(indata[:,0]*32767).astype(np.int16).tobytes()
            on_frames(pcm)
        self._in=sd.InputStream(device=self.in_dev, channels=1, samplerate=self.sr,
                                dtype='float32', callback=cb, blocksize=frames)
        self._in.start()

    def stop_capture(self):
        if self._in: self._in.stop(); self._in.close(); self._in=None

    def start_playback(self):
        self._out=sd.OutputStream(device=self.out_dev, channels=1, samplerate=self.sr,
                                  dtype='int16', blocksize=0)
        self._out.start()

    def play_bytes(self, pcm16:bytes):
        arr=np.frombuffer(pcm16, dtype=np.int16)
        self._out.write(arr)

    def stop_playback(self):
        if self._out: self._out.stop(); self._out.close(); self._out=None
