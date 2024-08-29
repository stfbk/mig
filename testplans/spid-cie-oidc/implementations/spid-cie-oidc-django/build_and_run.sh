#!/bin/bash

cd $(dirname "$0") # Go to directory containing script

git clone https://github.com/italia/spid-cie-oidc-django.git
rm ./spid-cie-oidc-django/docker-compose.yml
cp ./edited_files/docker-compose.yml ./spid-cie-oidc-django/
rm ./spid-cie-oidc-django/Dockerfile
cp ./edited_files/Dockerfile ./spid-cie-oidc-django/
cd spid-cie-oidc-django
bash docker-prepare.sh

# local build i-mig-t --------
cd ../../../../../tools/i-mig-t
# rm mig-t-beta-jar-with-dependencies.jar
sudo docker build -t i-mig-t .
cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/spid-cie-oidc-django/
# local build i-mig-t --------

# xhost +local:
sudo docker compose up -d --remove-orphans
wait
# host -local:
