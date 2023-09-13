#!/bin/bash
xhost +local:
cd spid-cie-oidc-django
docker compose up --remove-orphans
wait
xhost -local: