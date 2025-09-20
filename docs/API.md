# Add-on HTTP API

- `GET /api/health` → { model, input_device, output_device, sample_rate, latency_ms, mcp_enabled }
- `GET /api/devices` → ALSA-Geräteliste
- `POST /api/ptt/start` → Aufnahme/Streaming starten
- `POST /api/ptt/stop`  → Commit + response.create; Audioausgabe streamt

Auth: Basic (Default admin/ha, in Add-on Options konfigurierbar).
