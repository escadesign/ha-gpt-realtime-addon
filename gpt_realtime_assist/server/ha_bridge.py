import requests, json, time
from config import settings

class HABridge:
    def __init__(self):
        self.base=settings.ha_url.rstrip("/")
        self.headers={"Authorization":f"Bearer {settings.ha_token}","Content-Type":"application/json"}

    def call(self, domain:str, service:str, service_data:dict):
        url=f"{self.base}/api/services/{domain}/{service}"
        for _ in range(3):
            r=requests.post(url, headers=self.headers, data=json.dumps(service_data))
            if r.status_code in (200,201): return r.json()
            time.sleep(0.4)
        raise RuntimeError(f"HA call failed: {r.status_code} {r.text}")
