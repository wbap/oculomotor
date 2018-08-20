FROM ubuntu:xenial

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential software-properties-common cmake curl python3-dev \
    libgl1-mesa-dri libgl1-mesa-glx libglu1-mesa-dev xvfb x11-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip install --upgrade pip setuptools && \
    pip --no-cache-dir install \
    numpy==1.14.5 flask pygame opencv-python BriCA2 
    #chainer torch torchvision tensorflow 

ENV CONTAINER_APP /opt/oculomotor/application
ENV CONTAINER_TEST /opt/oculomotor/test

RUN mkdir -p ${CONTAINER_APP} ${CONTAINER_TEST}

ENV PYTHONPATH ${CONTAINER_APP}:${CONTAINER_TEST}
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 5000

ENV FLASK_APP ${CONTAINER_APP}/main.py
ENV FLASK_ENV development

ENV XVFB_WHD="1920x1080x24"
ENV DISPLAY=":99"

CMD ["flask", "run", "--host=0.0.0.0"]
