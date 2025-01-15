#!/bin/bash

cd $(dirname "$0") # Go to directory containing script

git clone https://github.com/italia/spid-cie-oidc-django.git
rm ./spid-cie-oidc-django/docker-compose.yml
cp ./edited_files/docker-compose-base.yml ./spid-cie-oidc-django/
cp ./edited_files/docker-compose.yml ./spid-cie-oidc-django/
cp ./edited_files/docker-compose-headless.yml ./spid-cie-oidc-django/
rm ./spid-cie-oidc-django/Dockerfile
cp ./edited_files/Dockerfile ./spid-cie-oidc-django/
cd spid-cie-oidc-django
bash docker-prepare.sh


# local build i-mig-t --------
# TODO: comment after release on registry
cd ../../../../../tools/i-mig-t
# rm mig-t-beta-jar-with-dependencies.jar
sudo docker build -t i-mig-t .
cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/spid-cie-oidc-django/
# local build i-mig-t --------

echo "HEADLESS_MODE $HEADLESS_MODE"
if [ $HEADLESS_MODE ]; 
then 
  # mandatory: use "detached" mode (-d option) for pipeline
  sudo docker compose -f docker-compose-headless.yml up --remove-orphans
  wait
else
  xhost +local:
  sudo docker compose up --remove-orphans
  wait
  xhost -local:
fi

