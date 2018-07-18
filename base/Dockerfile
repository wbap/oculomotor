FROM alpine:latest

ENV CPATH /usr/include/python3.6m

RUN apk add --no-cache \
    gcc g++ musl-dev \
    python3-dev py3-numpy py3-pillow && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    pip install --trusted-host pypi.python.org \
    flask \
    pybrica \
    chainer \
    http://download.pytorch.org/whl/cpu/torch-0.4.0-cp36-cp36m-linux_x86_64.whl \
    torchvision \
    https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.8.0-py3-none-any.whl && \
    rm -r /root/.cache 
