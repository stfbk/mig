#!/bin/bash

# Usage: ./generate_conf.sh TEMPLATE_PATH OUTPUT_PATH

TEMPLATE_PATH="$1"
OUTPUT_PATH="$2"

if [ -z "$TEMPLATE_PATH" ] || [ -z "$OUTPUT_PATH" ]; then
  echo "Usage: $0 TEMPLATE_PATH OUTPUT_PATH"
  exit 1
fi

# Copy template to output path
cp "$TEMPLATE_PATH" "$OUTPUT_PATH"

# Escape nginx $variables with placeholders
sed -i -e 's/\$remote_addr/__REMOTE_ADDR__/g' \
       -e 's/\$proxy_add_x_forwarded_for/__PROXY_ADD_X_FORWARDED_FOR__/g' \
       -e 's/\$host/__HOST__/g' \
       -e 's/\$sub/__SUB__/g' \
       -e 's/\$subdomain/__SUBDOMAIN__/g' \
       -e 's/\$server_port/__SERVER_PORT__/g' \
       -e 's/\$scheme/__SCHEME__/g' \
       -e 's/\$target_upstream_external/__TARGET_UPSTREAM_EXTERNAL__/g' \
       -e 's/\$target_upstream_internal/__TARGET_UPSTREAM_INTERNAL__/g' \
       -e 's/\$target_upstream/__TARGET_UPSTREAM__/g' \
       -e 's/\$remote_user/__REMOTE_USER__/g' \
       -e 's/\$time_local/__TIME_LOCAL__/g' \
       -e 's/\$request/__REQUEST__/g' \
       -e 's/\$status/__STATUS__/g' \
       -e 's/\$body_bytes_sent/__BODY_BYTES_SENT__/g' \
       -e 's/\$http_referer/__HTTP_REFERER__/g' \
       -e 's/\$http_user_agent/__HTTP_USER_AGENT__/g' \
       -e 's/\$upstream_addr/__UPSTREAM_ADDR__/g' \
       -e 's/\$upstream_status/__UPSTREAM_STATUS__/g' \
       -e 's/\$request_time/__REQUEST_TIME__/g' \
       -e 's/\$upstream_response_time/__UPSTREAM_RESPONSE_TIME__/g' \
       -e 's/\$log_502/__LOG_502__/g' "$OUTPUT_PATH"

# Debug step: show after placeholder replacement
if [ "$DEBUG_VOLUME" == "true" ]; then
  echo -e "\n\n-------------------------------\n"
  echo "After placeholder replacement:"
  cat "$OUTPUT_PATH"
fi

# Substitute environment variables
envsubst < "$OUTPUT_PATH" > "${OUTPUT_PATH}.tmp" && mv "${OUTPUT_PATH}.tmp" "$OUTPUT_PATH"

# Debug step: show after envsubst
if [ "$DEBUG_VOLUME" == "true" ]; then
  echo -e "\n\n-------------------------------\n"
  echo "After environment compilation:"
  cat "$OUTPUT_PATH"
fi

# Restore placeholders to original nginx variables
sed -i -e 's/__REMOTE_ADDR__/\$remote_addr/g' \
       -e 's/__PROXY_ADD_X_FORWARDED_FOR__/\$proxy_add_x_forwarded_for/g' \
       -e 's/__HOST__/\$host/g' \
       -e 's/__SUB__/\$sub/g' \
       -e 's/__SUBDOMAIN__/\$subdomain/g' \
       -e 's/__SERVER_PORT__/\$server_port/g' \
       -e 's/__SCHEME__/\$scheme/g' \
       -e 's/__TARGET_UPSTREAM_EXTERNAL__/\$target_upstream_external/g' \
       -e 's/__TARGET_UPSTREAM_INTERNAL__/\$target_upstream_internal/g' \
       -e 's/__TARGET_UPSTREAM__/\$target_upstream/g' \
       -e 's/__REMOTE_USER__/\$remote_user/g' \
       -e 's/__TIME_LOCAL__/\$time_local/g' \
       -e 's/__REQUEST__/\$request/g' \
       -e 's/__STATUS__/\$status/g' \
       -e 's/__BODY_BYTES_SENT__/\$body_bytes_sent/g' \
       -e 's/__HTTP_REFERER__/\$http_referer/g' \
       -e 's/__HTTP_USER_AGENT__/\$http_user_agent/g' \
       -e 's/__UPSTREAM_ADDR__/\$upstream_addr/g' \
       -e 's/__UPSTREAM_STATUS__/\$upstream_status/g' \
       -e 's/__REQUEST_TIME__/\$request_time/g' \
       -e 's/__UPSTREAM_RESPONSE_TIME__/\$upstream_response_time/g' \
       -e 's/__LOG_502__/\$log_502/g' "$OUTPUT_PATH"

# Final output for debug
if [ "$DEBUG_VOLUME" == "true" ]; then
  echo -e "\n\n-------------------------------\n"
  echo "Final conf file:"
  cat "$OUTPUT_PATH"
fi
