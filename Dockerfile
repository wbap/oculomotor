FROM wbap/oculomotor-base:latest

ENV CONTAINER_APP /opt/oculomotor/application
ENV CONTAINER_TEST /opt/oculomotor/test

RUN mkdir -p ${CONTAINER_APP} ${CONTAINER_TEST}

ENV PYTHONPATH ${CONTAINER_APP}:${CONTAINER_TEST}
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 5000

ENV FLASK_APP ${CONTAINER_APP}/server.py
ENV FLASK_ENV development

CMD ["flask", "run", "--host=0.0.0.0"]
