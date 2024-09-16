#!/bin/bash

# Initialize variables
PASSIVE_MODE=false
INPUT=""

# Function to print usage
print_usage() {
    echo "Usage: $0 [-p] <test.json|AA|OP|RP|SA|TA> [-p]"
    exit 1
}

# Parse options
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p)
            PASSIVE_MODE=true
            ;;
        *)
            if [[ -z "$INPUT" ]]; then
                INPUT="$1"
            else
                print_usage
            fi
            ;;
    esac
    shift
done

# Ensure an input is provided
if [[ -z "$INPUT" ]]; then
    print_usage
fi

# List of allowed strings
ALLOWED_STRINGS="OP RP TA"

# Convert the input to uppercase for case-insensitive matching
INPUT_UPPER=$(echo "$INPUT" | tr '[:lower:]' '[:upper:]')

# Function to execute tests from the given JSON file
execute_tests_from_json() {
    local TEST_FILE=$1

    if ! jq empty "$TEST_FILE" >/dev/null 2>&1; then
        echo "Error: The file $TEST_FILE is not a valid JSON."
        exit 1
    fi

    TEST_CONTENT=$(<"$TEST_FILE")

    # Print test content
    echo "Content of test:"
    echo "$TEST_CONTENT"
    echo    # Print a blank line for separation

    # Extract the sessions array from the JSON using jq
    RAW_SESSIONS=$(jq -r '.tests[].test.sessions[]' "$TEST_FILE")

    # Use a bash array to store unique sessions
    declare -A UNIQUE_SESSIONS
    SESSIONS=()

    for SESSION in $RAW_SESSIONS; do
        if [[ -z "${UNIQUE_SESSIONS[$SESSION]}" ]]; then
            UNIQUE_SESSIONS[$SESSION]=1
            SESSIONS+=("$SESSION")
        fi
    done

    # Check if sessions were extracted successfully
    if [ ${#SESSIONS[@]} -eq 0 ]; then
        echo "No sessions found or unable to extract sessions."
        exit 1
    fi

    # Print the extracted sessions and their content
    echo "Sessions:"
    for SESSION in "${SESSIONS[@]}"; do
        echo "Session: $SESSION"
        SESSION_FILE="./input/mig-t/sessions/$SESSION"
        if [ -f "$SESSION_FILE" ]; then
            SESSION_CONTENT=$(<"$SESSION_FILE")
            echo "Content of $SESSION:"
            echo "$SESSION_CONTENT"
        else
            echo "Error: Session file $SESSION does not exist."
        fi
        echo    # Print a blank line for separation
    done

    # Generate random username and password
    USERNAME=$(openssl rand -hex 8)
    PASSWORD=$(openssl rand -hex 8)

    # Register the user
    echo "Registering user..."
    curl -m 30 -X POST http://localhost:3000/users \
      -H "Content-Type: application/json" \
      -d "{\"name\": \"$USERNAME\", \"password\": \"$PASSWORD\"}"

    # Login and capture the token
    echo "Logging in and capturing token..."
    RESPONSE=$(curl -m 30 -s -X POST http://localhost:3000/users/login \
      -H "Content-Type: application/json" \
      -d "{\"name\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")

    # Extract the token from the response
    TOKEN=$(echo "$RESPONSE" | grep -o '"token": *"[^"]*' | grep -o '[^"]*$')

    # Sending session and test and capturing output
    echo "Sending session and test and capturing output..."
    curl -m 180 -X POST http://localhost:3000/send_message \
    -H "Content-Type: text/plain" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$SESSION_CONTENT&$TEST_CONTENT" > output.json
    echo "Output saved to output.json"
}

# Check if the input is one of the allowed strings (case insensitive)
if [[ "$ALLOWED_STRINGS" =~ $INPUT_UPPER ]]; then
    echo "Input is a valid string: $INPUT"

    # Define the path to the JSON file based on the input string
    if $PASSIVE_MODE; then
        TEST_FILE="./input/mig-t/tests/single/$INPUT_UPPER/All_${INPUT_UPPER}_Passive.json"
    else
        TEST_FILE="./input/mig-t/tests/single/$INPUT_UPPER/All_${INPUT_UPPER}.json"
    fi

    # Check if the test file exists
    if [ ! -f "$TEST_FILE" ]; then
        echo "Error: The test file $TEST_FILE does not exist."
        exit 1
    fi

    execute_tests_from_json "$TEST_FILE"
else
    # If not an allowed string, check if it is a file
    if [ -f "$INPUT" ]; then
        echo "Input is a JSON file."
        execute_tests_from_json "$INPUT"
    else
        echo "Error: The argument must be either a valid JSON file or one of [OP, RP, TA]."
        exit 1
    fi
fi
