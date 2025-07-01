# Minimal Ubuntu image. Was needed to circumvent the limitations imposed by keycloak's one.
FROM ubuntu:20.04

# Install all required packages
# ca-certificates is used to install the local rootCA certificate
RUN apt-get update && apt-get install -y \
    wget \
    openjdk-17-jdk \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Keycloak installation
RUN wget https://github.com/keycloak/keycloak/releases/download/24.0.1/keycloak-24.0.1.tar.gz -O /tmp/keycloak.tar.gz && \
    tar -xzvf /tmp/keycloak.tar.gz -C /opt/ && \
    mv /opt/keycloak-24.0.1 /opt/keycloak && \
    rm /tmp/keycloak.tar.gz

# Uninstall wget, it was only useful for keycloak's installation -> reduces attack's surface
RUN apt-get purge -y \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up its env variables so that the shell recognises its starting command
ENV KEYCLOAK_HOME=/opt/keycloak
ENV PATH="$KEYCLOAK_HOME/bin:$PATH"

# Set starting working dir
WORKDIR /opt/keycloak