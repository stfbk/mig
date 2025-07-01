#!/bin/bash
cd "$(dirname "$0")" || exit 1
# Local dns for split brain, the idea is to reroute everything locally to a nginx instance that terminates https redirects
envsubst < ./dnsmasq_local/dnsmasq.local.conf.template > ./dnsmasq_local/dnsmasq.local.conf

# Compile all session templates
SESSIONS_TEMPLATE_DIR="./input/mig-t/sessions/templates"
SESSIONS_COMPILED_DIR="./input/mig-t/sessions/compiled"

mkdir -p "$SESSIONS_COMPILED_DIR"

for template in "$SESSIONS_TEMPLATE_DIR"/*.template; do
  filename=$(basename "$template" .template)
  envsubst < "$template" > "$SESSIONS_COMPILED_DIR/$filename"
done
# Nginx configuration
bash ../generic_compile_nginx.sh ./nginx/nginx.conf.template ./nginx/nginx.conf &
wait