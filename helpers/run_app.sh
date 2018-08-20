#!/bin/sh

LOCAL_APP=${PWD}/application
LOCAL_TEST=${PWD}/test
CONTAINER_APP=/opt/oculomotor/application
CONTAINER_TEST=/opt/oculomotor/test

docker run -it -p 5000:5000 \
	-v ${LOCAL_APP}:${CONTAINER_APP} \
	-v ${LOCAL_TEST}:${CONTAINER_TEST} \
	wbap/oculomotor-server
