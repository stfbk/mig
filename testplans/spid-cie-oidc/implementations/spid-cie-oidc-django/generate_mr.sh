#!/bin/bash

if [ ! -d "testplan-to-mr" ]; then
	cd ../../../../tools/testplan-to-mr
	sudo docker build -t testplan-to-mr .
	cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django
fi

docker run \
	--rm \
	-v ${PWD}/../..:/testplan-to-mr/input \
	-v ${PWD}/input/mig-t/tests/single:/testplan-to-mr/machine-readable-testplan/single \
	testplan-to-mr 

# docker run \
# 	--rm \
# 	-v ${PWD}/..:/testplan-to-mr/human-readable-testplan \
# 	-v ${PWD}/machine-readable-testplan:/testplan-to-mr/machine-readable-testplan \
# 	-v ${PWD}/spid-cie-oidc-django/config/testplan-to-mr/templates:/testplan-to-mr/templates \
# 	testplan-to-mr

#docker run \
#	--rm \
#	-v ${PWD}/human-readable-testplan:/testAutomation/human-readable-testplan \
#	-v ${PWD}/machine-readable-testplan:/testAutomation/machine-readable-testplan \
#	ghcr.io/stfbk/idm-pentestingtool-testplan-to-mr:main

wait