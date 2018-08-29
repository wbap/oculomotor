#!/bin/sh

CONTAINER_APP=/opt/oculomotor

docker run -it -p 6006:6006 --rm -v ${PWD}:${CONTAINER_APP} --entrypoint "" wbap/oculomotor tensorboard --logdir=${CONTAINER_APP}/log
