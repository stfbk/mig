# Start from an Ubuntu 20.04 image. Was needed to circumvent the limitations imposed by oauth2proxy's one.
FROM ubuntu:20.04

# Install dependencies for Go installation and OAuth2 Proxy
# ca-certificates is used to install the local rootCA certificate
# curl needed for quality of life improvement related to startup.
# Could be removed to reduce attack surface.
RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    sudo \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Brings into the container the scripts that will later be executed
COPY healthchecks /healthchecks/

# Download and install Go 1.23.0
RUN wget https://go.dev/dl/go1.23.0.linux-amd64.tar.gz && \
    sudo tar -C /usr/local -xzf go1.23.0.linux-amd64.tar.gz && \
    rm go1.23.0.linux-amd64.tar.gz

# Set up Go environment variables
ENV GOPATH="/root/go"
ENV PATH="${PATH}:/usr/local/go/bin:${GOPATH}/bin"

# Install oauth2-proxy using Go
RUN GO111MODULE=on go install github.com/oauth2-proxy/oauth2-proxy/v7@latest

# Uninstall packages that are not needed at runtime -> reduces attack's surface
RUN export SUDO_FORCE_REMOVE=yes &&  \
    apt-get purge -y wget sudo \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
