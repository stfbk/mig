#!/bin/bash

# if builded locally
# if [ ! -d "testplan-to-mr" ]; then
#	cd ../../../../tools/testplan-to-mr
#	sudo docker build -t testplan-to-mr .
#	cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django
#fi

docker run \
	--rm \
	-v ${PWD}/../..:/testplan-to-mr/input \
	-v ${PWD}/input/mig-t/tests/single:/testplan-to-mr/machine-readable-testplan/single \
	ghcr.io/stfbk/mig-testplan-to-mr:latest # testplan-to-mr # if builded locally 

wait