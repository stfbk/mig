#!/bin/bash

#if builded locally
# if [ ! -d "testplan-to-mr" ]; then
# 	cd ../../../../tools/testplan-to-mr
# 	sudo docker build -t testplan-to-mr .
# 	cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django
# fi

#First volume is for **testplan.csv** input
#Second is for **templates** input
#Third is for output of **single** file
docker run \
	--rm \
	-v ${PWD}/../..:/testplan-to-mr/input \
	-v ${PWD}/:/testplan-to-mr/config_file/ \
	-v ${PWD}/input/mig-t/tests/single:/testplan-to-mr/tests/single \
	-v ${PWD}/input/mig-t/tests/manual:/testplan-to-mr/tests/manual \
	-v ${PWD}/input/mig-t/configured_tests:/testplan-to-mr/configured_tests \
	ghcr.io/stfbk/mig-testplan-to-mr:latest # testplan-to-mr # if builded locally 

wait