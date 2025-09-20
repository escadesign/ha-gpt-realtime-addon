# Realtime Assist Add-on (OpenAI gpt-realtime)

Supervisor Add-on für Home Assistant OS, das den OpenAI `gpt-realtime` Audiomodus mit ALSA-Ein-/Ausgabe (UR22 MKII) nutzt.

## Features
- Websocket-Verbindung zu `wss://api.openai.com/v1/realtime?model=gpt-realtime`
- Push-to-Talk via REST (`/api/ptt/start`, `/api/ptt/stop`)
- PCM16 @ 24 kHz In-/Output über ALSA, optimiert für Steinberg UR22 MKII
- Home Assistant Service-Tool `call_home_assistant` (REST oder MCP)
- HTTPS + Basic Auth (Optional Ingress)

## Verzeichnisstruktur
```
addon_repo/
├── repository.yaml           # Add-on Repository-Metadaten
├── gpt_realtime_assist/      # Add-on Ordner
│   ├── config.yaml           # Add-on Definition
│   ├── Dockerfile
│   ├── run.sh
│   ├── rootfs/
│   └── server/               # FastAPI + Audio Runtime
└── docs/                     # API/AUDIO Hinweise
```

## Installation (Kurzfassung)
1. Repo in Home Assistant Supervisor als Add-on Repository hinzufügen.
2. Add-on installieren, Optionen (`openai_api_key`, Audio-Geräte, Auth) setzen.
3. Add-on starten, `/api/health` prüfen.

Detailierte Schritte siehe `docs/`.

## Entwicklung
- Abhängigkeiten: `sounddevice`, `numpy`, `fastapi`, `websockets`, `aiohttp` u.a. (siehe `gpt_realtime_assist/server/requirements.txt`).
- Lokaler Start: `./gpt_realtime_assist/run.sh` verwendet denselben Bootstrap wie das Add-on.
- Audio-Devices via `arecord -l` / `aplay -l` prüfen.

## Lizenz
Siehe upstream `LICENSE` des Forks.
