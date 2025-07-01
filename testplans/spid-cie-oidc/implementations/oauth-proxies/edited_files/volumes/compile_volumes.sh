#!/bin/bash

cd "$(dirname "$0")" || exit 1 # Position inside the script directory

source ../.env # Import of env variables. They are used for compilation

if [ "$DEBUG_VOLUME" == "true" ]; then
  echo "DEBUG COMPILATION VOLUMES ENABLED"
fi

# Launch all needed compilation scripts, after each one restoring wd to use correct relative paths
# current_dir=$(pwd) and cd "$current_dir" are used to restore the working directory between different scripts
current_dir=$(pwd)
bash ./oauth2proxy_nginx/compile_volumes_oauth2proxy_nginx.sh &
wait
cd "$current_dir" || exit 1
current_dir=$(pwd)
bash ./keycloak_nginx/compile_volumes_keycloak_nginx.sh &
wait
cd "$current_dir" || exit 1
current_dir=$(pwd)
bash ./keycloak/compile_volumes_keycloak.sh &
wait
cd "$current_dir" || exit 1
current_dir=$(pwd)
bash ./oauth2proxy/compile_volumes_oauth2proxy.sh &
wait
cd "$current_dir" || exit 1
current_dir=$(pwd)
bash ./resourceserver_nginx/compile_volumes_resourceserver_nginx.sh &
wait
cd "$current_dir" || exit 1
current_dir=$(pwd)
bash ./burpsuite/compile_volumes_burpsuite.sh &
wait
cd "$current_dir" || exit 1




