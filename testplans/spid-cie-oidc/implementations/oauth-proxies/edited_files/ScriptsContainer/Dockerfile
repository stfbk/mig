# Docker image to execute phyton in a lightweight env
FROM python:3.10-slim
# Phyton will not write bytecode in the container -> will save memory
ENV PYTHONDONTWRITEBYTECODE=1
# If there is a print, do it immediately. Useful for debug
ENV PYTHONUNBUFFERED=1

# Sets the working directory inside the container
WORKDIR /app

# Brings into the container the scripts that will later be executed
COPY Scripts /app/

# Install the 'requests' package. Used to interact with Keycloak
RUN pip install --no-cache-dir requests


