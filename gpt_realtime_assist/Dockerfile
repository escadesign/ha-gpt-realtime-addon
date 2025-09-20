ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM ${BUILD_FROM}

ARG BUILD_VERSION
ARG BUILD_ARCH

RUN apk add --no-cache \
    bash jq curl tzdata \
    alsa-lib alsa-utils \
    portaudio portaudio-dev \
    ffmpeg \
    python3 py3-pip py3-aiohttp \

    build-base python3-dev musl-dev

WORKDIR /opt/app
COPY server/ /opt/app/
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY rootfs/ /
ENV PYTHONUNBUFFERED=1
