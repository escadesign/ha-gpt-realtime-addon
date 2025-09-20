from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config import settings
from audio_io import AudioIO
from realtime_client import RealtimeClient
import uvicorn, asyncio

app=FastAPI()
security=HTTPBasic()
state={"latency_ms":None}
loop=asyncio.get_event_loop()
audio=AudioIO(settings.sample_rate, settings.input_device, settings.output_device)
client=RealtimeClient(audio, on_latency=lambda ms: state.__setitem__("latency_ms", ms))

def check(creds: HTTPBasicCredentials = Depends(security)):
    if not settings.require_auth: return
    if creds.username!=settings.api_username or creds.password!=settings.api_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.on_event("startup")
async def startup():
    await client.connect()
    audio.start_playback()

@app.post("/api/ptt/start")
async def ptt_start(credentials: HTTPBasicCredentials = Depends(check)):
    await client.ptt_start()
    return {"ok":True}

@app.post("/api/ptt/stop")
async def ptt_stop(credentials: HTTPBasicCredentials = Depends(check)):
    await client.ptt_stop_and_respond()
    return {"ok":True}

@app.get("/api/devices")
async def devices(credentials: HTTPBasicCredentials = Depends(check)):
    return {"devices": audio.list_devices()}

@app.get("/api/health")
async def health():
    return {
      "model":"gpt-realtime",
      "connected_openai": True,
      "input_device": settings.input_device,
      "output_device": settings.output_device,
      "sample_rate": settings.sample_rate,
      "latency_ms": state["latency_ms"],
      "mcp_enabled": settings.mcp_enabled
    }

def run():
    uvicorn.run(app, host="0.0.0.0", port=8443)

if __name__=="__main__":
    run()
