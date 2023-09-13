#!/bin/bash
# Check if the directory exists
if [ ! -d "spid-cie-oidc-django" ]; then
  # Removed unused containers
  docker container prune -f
  # Check if there are old images and remove it
  docker rmi proxy -f
  docker rmi ghcr.io/italia/spid-cie-oidc-django -f
  # Clone the directory
  git clone git@github.com:italia/spid-cie-oidc-django.git
  # Build the environment
  rm ./spid-cie-oidc-django/docker-compose.yml
  cp docker-compose.yml ./spid-cie-oidc-django/
  cd spid-cie-oidc-django
  bash docker-prepare.sh
  cd ../
fi
# Check if images exists
if [[ ! -n "$(docker images -a | grep -E proxy)" ]] || [[ ! -n "$(docker images -a | grep -E ghcr.io/italia/spid-cie-oidc-django)" ]]; then
  # Removed unused containers
  docker container prune -f
  # Check if there are old images and remove it
  docker rmi proxy -f
  docker rmi ghcr.io/italia/spid-cie-oidc-django -f
  # Build images
  cd burpsuite_container
  docker build -t proxy .
  cd ../
fi

# Run
xhost +local:
cd spid-cie-oidc-django
docker-compose up --remove-orphans
wait
xhost -local:
