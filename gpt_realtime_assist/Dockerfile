ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    bash jq curl tzdata \
    alsa-lib alsa-utils \
    portaudio portaudio-dev \
    ffmpeg \
    python3 py3-pip py3-aiohttp py3-websockets

WORKDIR /opt/app
COPY server/ /opt/app/
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

COPY rootfs/ /
ENV PYTHONUNBUFFERED=1
