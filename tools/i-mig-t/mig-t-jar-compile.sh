#!/bin/bash

# compile mig-t jar ---------
cd "$(dirname "$0")" # go to script's directory
cd ../
git submodule update --init
cd mig-t/tool/
mvn package
cp target/mig-t-beta-jar-with-dependencies.jar ../../i-mig-t/
cd ../../i-mig-t/
# compile mig-t jar ---------