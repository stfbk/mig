#!/bin/bash

cd $(dirname "$0") # Go to directory containing script

#if builded locally
if [ ! -d "testplan-to-mr" ]; then
	cd ../../../../tools/testplan-to-mr
	sudo docker build -t testplan-to-mr .
	cd ../../testplans/spid-cie-oidc/implementations/spid-cie-oidc-django
fi

#Check if the flag exist
justFillFlag=""
djangoFlag=""
while [[ $# -gt 0 ]]; do
	key="$1"
	case $key in
		--justFill)
			if [[ -n "$2" ]]; then
				justFillFlag="--justFill $2"
				folder_path="$2"
				shift 2
			else
				echo "Error: Missing argument for --justFill"
				exit 1
			fi
			;;
		--django)
			djangoFlag="--django"
			shift
			;;
		*)
			echo "Error: Unknown option $key"
			exit 1
			;;
	esac
done

#Add the volume only if exist
volume_mount=""
if [ -n "$justFillFlag" ]; then
	volume_mount="-v ${PWD}/$folder_path:/testplan-to-mr/$folder_path"
fi

#First volume is for **/../testplan.csv** and **/config/testplan-to-mr/templates** input
#Second is for the **templates**
#Third is for **/config_testplan.json** input
#Fourth is for output of **/input/mig-t/tests/single** file
#Fifth is for output of **/input/mig-t/tests/manual** file
#Sixth is for output of **/input/mig-t/tests/configured_tests** tests

docker run \
	--rm \
	-v ${PWD}/../../testplan.csv:/testplan-to-mr/input/testplan.csv \
	-v ${PWD}/../../config/testplan-to-mr/templates/:/testplan-to-mr/input/templates/ \
	-v ${PWD}/config/testplan-to-mr:/testplan-to-mr/config_file/ \
	-v ${PWD}/input/mig-t/tests/single:/testplan-to-mr/tests/single \
	-v ${PWD}/input/mig-t/tests/manual:/testplan-to-mr/tests/manual \
	-v ${PWD}/input/mig-t/configured_tests:/testplan-to-mr/configured_tests \
	$volume_mount \
	testplan-to-mr /bin/bash -c "python testplan-to-mr.py $justFillFlag $djangoFlag"

wait