import base64, time
def b64_pcm(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")
class Stopwatch:
    def __init__(self): self.t0=None
    def start(self): self.t0=time.perf_counter()
    def stop(self):  return (time.perf_counter()-self.t0)*1000 if self.t0 else None
