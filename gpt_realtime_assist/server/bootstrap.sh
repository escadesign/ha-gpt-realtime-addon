#!/usr/bin/env bash
set -e
CONFIG=/data/options.json

OPENAI_API_KEY=$(jq -r '.openai_api_key' $CONFIG)
HA_URL=$(jq -r '.ha_url' $CONFIG)
HA_TOKEN=$(jq -r '.ha_token' $CONFIG)
LANGUAGE=$(jq -r '.language' $CONFIG)
VOICE=$(jq -r '.voice' $CONFIG)
SAMPLE_RATE=$(jq -r '.sample_rate' $CONFIG)
IN_DEV=$(jq -r '.input_device' $CONFIG)
OUT_DEV=$(jq -r '.output_device' $CONFIG)
TLS=$(jq -r '.tls' $CONFIG)
REQ_AUTH=$(jq -r '.require_auth' $CONFIG)
USER=$(jq -r '.username' $CONFIG)
PASS=$(jq -r '.password' $CONFIG)
MCP=$(jq -r '.mcp_enabled' $CONFIG)

cat >/opt/app/.env <<EOF_ENV
OPENAI_API_KEY=${OPENAI_API_KEY}
HA_URL=${HA_URL}
HA_TOKEN=${HA_TOKEN}
LANGUAGE=${LANGUAGE}
VOICE=${VOICE}
SAMPLE_RATE=${SAMPLE_RATE}
INPUT_DEVICE=${IN_DEV}
OUTPUT_DEVICE=${OUT_DEV}
REQUIRE_AUTH=${REQ_AUTH}
API_USERNAME=${USER}
API_PASSWORD=${PASS}
MCP_ENABLED=${MCP}
EOF_ENV

# ensure ALSA default uses configured card if plughw/hw is specified
ASOUND_RC=/root/.asoundrc
CARD_NAME=
if [[ "$IN_DEV" =~ CARD=([^,]+) ]]; then
  CARD_NAME="${BASH_REMATCH[1]}"
elif [[ "$IN_DEV" == hw:* || "$IN_DEV" == plughw:* ]]; then
  CARD_NAME="$(echo "$IN_DEV" | cut -d':' -f2 | cut -d',' -f1)"
fi

if [ -n "$CARD_NAME" ]; then
  cat >"$ASOUND_RC" <<EOF_ASOUND
defaults.pcm.card $CARD_NAME
defaults.pcm.device 0
defaults.ctl.card $CARD_NAME
EOF_ASOUND
fi
