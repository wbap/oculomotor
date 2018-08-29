#!/bin/sh

LOCAL_APP=${PWD}/application
CONTAINER_APP=/opt/oculomotor

docker run -it -p 5000:5000 --rm -v ${PWD}:${CONTAINER_APP} wbap/oculomotor
