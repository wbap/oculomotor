#!/bin/sh

CONTAINER_APP=/opt/oculomotor

docker run -it -v ${PWD}:${CONTAINER_APP} wbap/oculomotor python ${CONTAINER_APP}/application/train.py $*

