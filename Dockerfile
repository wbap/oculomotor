FROM ubuntu:xenial

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential software-properties-common cmake curl python3-dev \
    libgl1-mesa-dri libgl1-mesa-glx libglu1-mesa-dev xvfb x11-utils libasio-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

COPY requirements.txt /tmp

RUN pip install --upgrade pip setuptools && \
    pip --no-cache-dir install -r /tmp/requirements.txt

ENV CONTAINER_APP /opt/oculomotor
WORKDIR ${CONTAINER_APP}

ENV PYTHONPATH ${CONTAINER_APP}/application:${CONTAINER_APP}/test
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 5000 6006

ENV FLASK_APP ${CONTAINER_APP}/application/server
ENV FLASK_ENV development

ENV XVFB_WHD="1920x1080x24"
ENV DISPLAY=":99"

ENTRYPOINT ["/opt/oculomotor/helpers/entrypoint.sh"]

CMD ["flask", "run", "--host=0.0.0.0"]
