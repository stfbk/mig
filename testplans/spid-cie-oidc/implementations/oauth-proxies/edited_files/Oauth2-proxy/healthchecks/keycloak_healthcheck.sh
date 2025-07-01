#!/bin/bash

# HTTP status codes
HTTP_OK=200
HTTP_UNAUTHORIZED=401

check_keycloak() {
    # Step 1: Readiness health check
    health_url="${KEYCLOAK_URL}/health/ready"
    health_response=$(curl -s -o response.txt -w "%{http_code}" "$health_url")

    if [ "$health_response" -eq "$HTTP_OK" ]; then
        # Extract the value of the "status" field without jq
        status=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' response.txt | sed -E 's/.*"status"[[:space:]]*:[[:space:]]*"([^"]*)".*/\1/')

        if [ "$status" == "UP" ]; then
            echo "Keycloak is healthy and ready."

            # Step 2: Check server info endpoint
            serverinfo_url="${KEYCLOAK_URL}/admin/serverinfo"
            serverinfo_response=$(curl -s -o response.txt -w "%{http_code}" "$serverinfo_url")

            if [ "$serverinfo_response" -eq "$HTTP_UNAUTHORIZED" ]; then
                echo "Keycloak is running but requires authentication for /admin/serverinfo."
                return 0
            elif [ "$serverinfo_response" -eq "$HTTP_OK" ]; then
                echo "Keycloak /admin/serverinfo accessible without auth (unexpected)."
                return 0
            else
                echo "Unexpected status from /admin/serverinfo: $serverinfo_response"
            fi
        else
            echo "Keycloak health check failed: status != 'UP' (got: $status)"
        fi
    else
        echo "Keycloak health check failed. Status: $health_response"
    fi

    return 1
}

# Run indefinitely until the check returns true
while true; do
    check_keycloak
    result=$?

    if [ "$result" -eq 0 ]; then
        echo "Exiting: Keycloak health check succeeded."
        break
    else
        echo "Keycloak health check failed. You should start Burp. Retrying in ${KEYCLOAK_HEALTH_CHECK_INTERVAL}..."
    fi

    # Sleep for a defined interval before retrying
    sleep "${KEYCLOAK_HEALTH_CHECK_INTERVAL}"
done