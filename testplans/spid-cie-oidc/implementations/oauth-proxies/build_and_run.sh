#!/bin/bash

# Install dependencies for compilation. For future deployments, it could be possible to use a dedicated container! So no dependencies on host machine
dpkg -l | grep -q gettext || sudo apt install -y gettext
dpkg -l | grep -q sed || sudo apt install -y sed
dpkg -l | grep -q openssl || sudo apt install -y openssl

cd "$(dirname "$0")" || exit 1 # Go to directory containing script


current_dir=$(pwd)
bash ./edited_files/volumes/compile_volumes.sh & # Execute compilation and wait for its completion
wait
cd "$current_dir" || exit 1
current_dir=$(pwd)
bash ./edited_files/volumes/CA/generate_keys_OpenSSL.sh & # Creates private key and signs
wait


# Start docker compose
cd ./edited_files || exit 1
xhost +local:
sudo docker compose up --remove-orphans &
wait
xhost -local: