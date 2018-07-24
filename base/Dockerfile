FROM ubuntu:xenial

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential software-properties-common cmake curl python3-dev && \
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
    numpy \
    pybrica \
    flask \
    chainer \
    torch \
    torchvision \
    tensorflow \
    opencv-python
