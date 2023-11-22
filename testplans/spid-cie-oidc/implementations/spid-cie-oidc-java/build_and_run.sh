#!/bin/bash

# clone and build spid-cie-oidc-django ---
git clone https://github.com/italia/spid-cie-oidc-django.git
cd spid-cie-oidc-django/
git checkout 7e15d4b2b96c805208395ce66ab98465fe0d1463
cd ..
rm ./spid-cie-oidc-django/docker-compose.yml
cp docker-compose.yml ./spid-cie-oidc-django/
rm ./spid-cie-oidc-django/examples/federation_authority/dumps/examples.json
cp example.json ./spid-cie-oidc-django/examples/federation_authority/dumps/
cd spid-cie-oidc-django
bash docker-prepare.sh
cd ..
# clone and build spid-cie-oidc-django ---

# (Optional) Build your RP image here ---
git clone git@github.com:italia/spid-cie-oidc-java.git
rm spid-cie-oidc-java/examples/relying-party-spring-boot/docker/Dockerfile.java-rp
cp Dockerfile.java-rp spid-cie-oidc-java/examples/relying-party-spring-boot/docker/
cd spid-cie-oidc-java/examples/relying-party-spring-boot/docker
sudo docker build -t your-rp --file Dockerfile.java-rp .
cd ../../../../spid-cie-oidc-django
# (Optional) Build your RP image here ---

# local build i-mig-t --------
cd ../../../../../tools/i-mig-t
sudo docker build -t i-mig-t .
cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-java/spid-cie-oidc-django/
# local build i-mig-t --------

xhost +local:
sudo docker compose up
wait
xhost -local:
