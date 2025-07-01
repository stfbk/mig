# Start from Python 3.10 slim image
FROM python:3.10-slim

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libssl-dev libffi-dev build-essential \
    ca-certificates curl bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy application code inside
COPY Scripts /app/
COPY servedFiles /webOrigin/

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn[standard] httpx python-jose[cryptography] jinja2

# Makes sure the container will update CA certificates at runtime
RUN mkdir -p /usr/local/share/ca-certificates /etc/ssl/certs /etc/ssl/private