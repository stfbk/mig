#!/bin/bash
git clone https://github.com/italia/spid-cie-oidc-django.git
rm ./spid-cie-oidc-django/docker-compose.yml
cp docker-compose.yml ./spid-cie-oidc-django/
cd spid-cie-oidc-django
bash docker-prepare.sh

# Unnecessary part if image hosted in github --------
cd ../../../../../tools/i-mig-t
#rm mig-t-beta-jar-with-dependencies.jar
sudo docker build -t i-mig-t .
cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/spid-cie-oidc-django/
# Unnecessary part if image hosted in github --------

xhost +local:
sudo docker compose up --remove-orphans
wait
xhost -local:
