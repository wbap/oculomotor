#!/bin/sh

docker run -it -p 8080:80 -v ${PWD}/application/log:/application/log wbap/oculomotor-server
