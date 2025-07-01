# Start from an Ubuntu 20.04 image
FROM ubuntu:20.04

# Networking utils to handle the network:
# Redsocks and iptables to make everything go through Burp
# Dnsmasq and nginx to handle incoming connection from the outside
# ca-certificates is used to install the local rootCA certificate
RUN apt-get update && \
    apt-get install -y \
    redsocks \
    iptables \
    nginx \
    dnsmasq \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*