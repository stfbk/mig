#!/bin/bash
cd "$(dirname "$0")" || exit 1
# Config file of oauth2proxy
envsubst < ./config/oauth2proxy.toml.template > ./config/oauth2proxy.toml
wait