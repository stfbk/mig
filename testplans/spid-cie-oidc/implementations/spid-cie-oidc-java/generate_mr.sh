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
	-v ${PWD}/config/testplan-to-mr/templates:/testplan-to-mr/input/templates \
	-v ${PWD}/input/mig-t/tests/single:/testplan-to-mr/machine-readable-testplan/single \
	ghcr.io/stfbk/mig-testplan-to-mr:latest # testplan-to-mr # if builded locally 

wait