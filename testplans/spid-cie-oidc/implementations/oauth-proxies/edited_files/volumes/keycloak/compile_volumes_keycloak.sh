#!/bin/bash
cd "$(dirname "$0")" || exit 1
# Config file of keycloak
envsubst < ./config/keycloak.conf.template > ./config/keycloak.conf
wait