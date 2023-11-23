#!/bin/bash

# clone and build spid-cie-oidc-django ---
git clone https://github.com/italia/spid-cie-oidc-django.git
rm ./spid-cie-oidc-django/docker-compose.yml
cp docker-compose.yml ./spid-cie-oidc-django/
cd spid-cie-oidc-django
bash docker-prepare.sh
# clone and build spid-cie-oidc-django ---

# (Optional) Build your RP image here ---
#git clone yourrepo.git
#sudo docker build -t your-rp .
# (Optional) Build your RP image here ---

# local build i-mig-t --------
#cd ../../../../../tools/i-mig-t
#rm mig-t-beta-jar-with-dependencies.jar
#cp /home/bit/FBK/mig-t/tool/target/mig-t-beta-jar-with-dependencies.jar .
#sudo docker build -t i-mig-t .
#cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django/spid-cie-oidc-django/ # TODO: change to your folder
# local build i-mig-t --------

xhost +local:
sudo docker compose up --remove-orphans
wait
xhost -local:
