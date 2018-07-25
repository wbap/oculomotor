#!/bin/bash

HOST_APP=`pwd`/../application
CONTAINER_APP=/opt/oculomotor/application
HOST_TEST=`pwd`/../test
CONTAINER_TEST=/opt/oculomotor/test

CONTAINER_BIN=/opt/oculomotor/bin
DEUBG_SERVER=${CONTAINER_BIN}/debug_server.sh

docker run --rm -it -d -v ${HOST_APP}:${CONTAINER_APP} -v ${HOST_TEST}:${CONTAINER_TEST} -p 3000:3000 -p 8080:80 oculomotor-debug:latest ${DEUBG_SERVER}
