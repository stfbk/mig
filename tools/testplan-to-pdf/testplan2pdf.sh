#!/bin/bash

if [ ! -d "testplan-to-pdf" ]; then
	sudo docker build -t testplan-to-pdf .
fi

docker run \
	--rm \
	-v ${PWD}/../../testplans/spid-cie-oidc/:/testplan-to-pdf/input \
    -v ${PWD}/output:/testplan-to-pdf/output \
	testplan-to-pdf

wait