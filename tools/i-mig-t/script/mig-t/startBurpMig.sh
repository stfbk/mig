#!/bin/bash

echo "*************************************"
echo "HEADLESS_MODE enabled $HEADLESS_MODE"
echo "*************************************"

if [ $HEADLESS_MODE ]; then 
    # Set environment variable to run Firefox in headless mode
    echo "Set environment variable to run Firefox in headless mode"
    export MOZ_HEADLESS=1
fi

# To disable headless mode remove -Djava.awt.headless=true
echo 'y' | java -Djava.awt.headless=$HEADLESS_MODE -jar \
/opt/BurpSuiteCommunity/burpsuite_community.jar \
--user-config-file="/opt/BurpSuiteCommunity/user-options.json" \
--config-file="/opt/BurpSuiteCommunity/project-options.json"

