import asyncio, json, websockets, base64
from typing import Callable
from config import settings
from util import b64_pcm, Stopwatch
from ha_bridge import HABridge

REALTIME_URL="wss://api.openai.com/v1/realtime?model=gpt-realtime"

class RealtimeClient:
    def __init__(self, audio, on_latency:Callable[[float],None]):
        self.audio=audio; self.on_latency=on_latency
        self.ws=None; self.listening=False; self.speaking=False
        self.ha=HABridge()

    async def connect(self):
        self.ws=await websockets.connect(
            REALTIME_URL,
            extra_headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "OpenAI-Beta": "realtime=v1"
            },
            max_size=20*1024*1024,
        )
        await self.session_update()
        asyncio.create_task(self.recv_loop())

    async def session_update(self):
        payload={
          "type":"session.update",
          "session":{
            "instructions":"Sprich Deutsch, antworte kurz, freundlich. Wenn der Nutzer Gerätebefehle äußert, nutze das Tool.",
            "input_audio_format":"pcm16",
            "input_sample_rate_hz":settings.sample_rate,
            "output_audio_format":"pcm16",
            "voice":settings.voice,
            "turn_detection":{"type":"none"},
            "tools":[
              {
                "name":"call_home_assistant","type":"function",
                "description":"Call a Home Assistant service",
                "parameters":{
                  "type":"object",
                  "properties":{
                    "domain":{"type":"string"},
                    "service":{"type":"string"},
                    "service_data":{"type":"object"}
                  },
                  "required":["domain","service"]
                }
              }
            ]
          }
        }
        await self.ws.send(json.dumps(payload))

    async def recv_loop(self):
        sw=None
        while True:
            msg=await self.ws.recv()
            if isinstance(msg, bytes):
                self.audio.play_bytes(msg); continue
            data=json.loads(msg); t=data.get("type")

            if t=="response.output_audio.delta":
                self.audio.play_bytes(base64.b64decode(data["delta"]))
            elif t=="response.started":
                self.speaking=True; sw=Stopwatch(); sw.start()
            elif t in ("response.completed","response.finished"):
                self.speaking=False
                if sw: self.on_latency(sw.stop() or 0)
            elif t=="response.cancelled":
                self.speaking=False
            elif t=="conversation.item.call_tool":
                if data.get("name")=="call_home_assistant":
                    args=data.get("arguments",{})
                    try:
                        res=self.ha.call(args["domain"], args["service"], args.get("service_data",{}))
                        await self.ws.send(json.dumps({
                          "type":"conversation.item.create",
                          "item":{"type":"function_call_output","call_id":data.get("call_id",""),"output":json.dumps(res)}
                        }))
                        await self.ws.send(json.dumps({"type":"response.create"}))
                    except Exception as e:
                        await self.ws.send(json.dumps({
                          "type":"conversation.item.create",
                          "item":{"type":"function_call_output","call_id":data.get("call_id",""),"output":f"ERROR {e}"}
                        }))
                        await self.ws.send(json.dumps({"type":"response.create"}))

    async def _send_audio(self, pcm:bytes):
        await self.ws.send(json.dumps({"type":"input_audio_buffer.append","audio": b64_pcm(pcm)}))

    async def ptt_start(self):
        self.listening=True
        def cb(pcm:bytes):
            if self.listening:
                asyncio.run_coroutine_threadsafe(self._send_audio(pcm), asyncio.get_event_loop())
        self.audio.start_capture(cb)

    async def ptt_stop_and_respond(self):
        self.listening=False; self.audio.stop_capture()
        await self.ws.send(json.dumps({"type":"input_audio_buffer.commit"}))
        await self.ws.send(json.dumps({"type":"response.create","response":{"modalities":["audio"]}}))

    async def cancel(self):
        if self.speaking:
            await self.ws.send(json.dumps({"type":"response.cancel"}))
            self.speaking=False
