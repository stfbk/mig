#!/bin/bash
cd "$(dirname "$0")" || exit 1
# External dns for client
envsubst < ./dnsmasq_external/dnsmasq.external.conf.template > ./dnsmasq_external/dnsmasq.external.conf
# Internal dns for private network
envsubst < ./dnsmasq_internal/dnsmasq.internal.conf.template > ./dnsmasq_internal/dnsmasq.internal.conf
# Local dns for split brain, internal for nginx when rerouting
envsubst < ./dnsmasq_local/dnsmasq.local.conf.template > ./dnsmasq_local/dnsmasq.local.conf
# Nginx configuration
bash ../generic_compile_nginx.sh ./nginx/nginx.conf.template ./nginx/nginx.conf &
wait