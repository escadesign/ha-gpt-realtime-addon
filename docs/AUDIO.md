# Audio / UR22 MKII

- Devices prüfen:
  - Host-Shell: `arecord -l` / `aplay -l`
- ALSA Device Strings:
  - `plughw:CARD=UR22mkII,DEV=0`
- Latenz:
  - Ethernet statt WLAN, kein Bluetooth-Audio
  - 24 kHz PCM16, Chunk-Größe 20–40 ms
  - PTT (manuell) = geringere Fehltrigger, schnellere Runden
