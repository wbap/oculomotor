FROM wbap/oculomotor-base:latest

ENV CONTAINER_APP /opt/oculomotor/application
ENV CONTAINER_TEST /opt/oculomotor/test

RUN mkdir -p ${CONTAINER_APP} ${CONTAINER_TEST}
ADD ./application ${CONTAINER_APP}
ADD ./test ${CONTAINER_TEST}

ENV PYTHONPATH ${CONTAINER_APP}:${CONTAINER_TEST}

EXPOSE 80

CMD ["python", "${CONTAINER_APP}/server.py"]
