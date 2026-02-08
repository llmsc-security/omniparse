# syntax=docker/dockerfile:1.4

# ------------------------------------------------------------
# Build arguments - defined once at the top of the file
# ------------------------------------------------------------
ARG CUDA_VERSION="11.8.0"
ARG CUDNN_VERSION="8"
ARG UBUNTU_VERSION="22.04"

# ------------------------------------------------------------
# Builder stage - installs all heavy system packages, Chrome,
# ChromeDriver and Python wheels (torch, transformers, etc.)
# ------------------------------------------------------------
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-devel-ubuntu${UBUNTU_VERSION} AS builder

# System utilities + Chrome dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget curl unzip git python3 python3-pip \
        libgl1 libglib2.0-0 gnupg2 ca-certificates \
        apt-transport-https software-properties-common \
        libreoffice ffmpeg git-lfs xvfb \
        fonts-liberation libu2f-udev libvulkan1 && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# ChromeDriver - install via apt for better compatibility
RUN apt-get update && \
    apt-get install -y --no-install-recommends chromium-chromedriver && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Python tooling & heavy wheels (torch, transformers)
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=1200
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir torch torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu118 && \
    pip3 install --no-cache-dir transformers==4.41.2

# ------------------------------------------------------------
# Runtime stage - minimal image, copy only what we need
# ------------------------------------------------------------
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-runtime-ubuntu${UBUNTU_VERSION} AS runtime

# Install python3, pip, and runtime libraries required by Chrome
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip \
        libgl1 libglib2.0-0 ca-certificates fonts-liberation libu2f-udev libvulkan1 xvfb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy Chrome, ChromeDriver from builder
COPY --from=builder /usr/bin/google-chrome /usr/bin/google-chrome
COPY --from=builder /usr/share/keyrings/google-chrome.gpg /usr/share/keyrings/google-chrome.gpg
COPY --from=builder /etc/apt/sources.list.d/google-chrome.list /etc/apt/sources.list.d/google-chrome.list
COPY --from=builder /usr/bin/chromedriver /usr/bin/chromedriver

# Copy pip-installed packages from builder to runtime
COPY --from=builder /usr/local/lib/python3.*/dist-packages /usr/local/lib/python3.*/dist-packages

# Application code
WORKDIR /app
COPY . /app

# Install remaining Python dependencies (excluding flash-attn which requires compilation)
RUN pip3 install --no-cache-dir packaging && pip3 install --no-cache-dir -r requirements.txt

# Install the local package (editable, no re-download of deps)
RUN pip3 install --no-cache-dir -e . --no-deps

# Environment variables used by Selenium / the app
ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROMEDRIVER=/usr/bin/chromedriver \
    DISPLAY=:99 \
    DBUS_SESSION_BUS_ADDRESS=/dev/null \
    PYTHONUNBUFFERED=1 \
    PATH=/usr/local/bin:$PATH

# Logging directory & exposed port
RUN mkdir -p /var/log && touch /var/log/app.log
EXPOSE 8000

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
