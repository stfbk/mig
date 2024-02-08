#!/bin/bash

cd $(dirname "$0") # Go to directory containing script

# clone and build spid-cie-oidc-django ---
git clone https://github.com/italia/spid-cie-oidc-django.git
rm ./spid-cie-oidc-django/docker-compose.yml
cp edited_files/docker-compose.yml ./spid-cie-oidc-django/
rm ./spid-cie-oidc-django/Dockerfile
cp edited_files/Dockerfile ./spid-cie-oidc-django/
rm ./spid-cie-oidc-django/examples/federation_authority/dumps/examples.json
cp edited_files/example.json ./spid-cie-oidc-django/examples/federation_authority/dumps/
cd spid-cie-oidc-django
bash docker-prepare.sh
cd ..
# clone and build spid-cie-oidc-django ---

# (Optional) Build your RP image here ---
git clone git@github.com:italia/spid-cie-oidc-java.git
rm spid-cie-oidc-java/examples/relying-party-spring-boot/docker/Dockerfile.java-rp
cp edited_files/Dockerfile.java-rp spid-cie-oidc-java/examples/relying-party-spring-boot/docker/
cd spid-cie-oidc-java/examples/relying-party-spring-boot/docker
sudo docker build -t your-rp --file Dockerfile.java-rp .
cd ../../../../spid-cie-oidc-django
# (Optional) Build your RP image here ---

# local build i-mig-t --------
cd ../../../../../tools/i-mig-t
# rm mig-t-beta-jar-with-dependencies.jar
# bash mig-t-jar-compile.sh # To complie mig-t to the last version
sudo docker build -t i-mig-t .
cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-java/spid-cie-oidc-django/
# local build i-mig-t --------

xhost +local:
sudo docker compose up
wait
xhost -local:
