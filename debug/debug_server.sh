#!/bin/sh

sleep 3

APP_PATH=/opt/oculomotor/application
if [ ${APP_PATH}/debug.py ]; then
  /usr/bin/python ${APP_PATH}/debug.py
fi
