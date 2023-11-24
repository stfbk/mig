#!/bin/bash

#if builded locally
if [ ! -d "testplan-to-mr" ]; then
	cd ../../../../tools/testplan-to-mr
	sudo docker build -t testplan-to-mr .
	cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django # TODO change with the name of your folder
fi

#First volume is for **/../testplan.csv** and **/config/testplan-to-mr/templates** input
#Second is for **/config_testplan.json** input
#Third is for output of **/input/mig-t/tests/single** file
#Fourth is for output of **/input/mig-t/tests/manual** file
#Fifth is for output of **/input/mig-t/tests/configured_tests** tests

docker run \
	--rm \
	-v ${PWD}/../../testplan.csv:/testplan-to-mr/input/testplan.csv \
	-v ${PWD}/../../config/testplan-to-mr/templates/:/testplan-to-mr/input/templates/ \
	-v ${PWD}/config/testplan-to-mr:/testplan-to-mr/config_file/ \
	-v ${PWD}/input/mig-t/tests/single:/testplan-to-mr/tests/single \
	-v ${PWD}/input/mig-t/tests/manual:/testplan-to-mr/tests/manual \
	-v ${PWD}/input/mig-t/configured_tests:/testplan-to-mr/configured_tests \
	ghcr.io/stfbk/mig-testplan-to-mr:latest # testplan-to-mr # local image 

wait