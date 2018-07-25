FROM oculomotor-base:latest

# set up launch configuration
# todo: decide path configuration
ENV APP_PATH /opt/oculomotor/application
ENV TEST_PATH /opt/oculomotor/test

RUN mkdir -p ${APP_PATH} ${TEST_PATH}

ENV PYTHONPATH ${APP_PATH}:${TEST_PATH}

# ptvsd: remote debug module
RUN pip --no-cache-dir install ptvsd==3.0.0

# volume config
ENV CONTAINER_BIN /opt/oculomotor/bin
RUN mkdir -p ${CONTAINER_BIN}
COPY ./debug_server.sh ${CONTAINER_BIN}
RUN chmod 755 ${CONTAINER_BIN}/debug_server.sh

# open flask and ptvsd port
EXPOSE 80
EXPOSE 3000
