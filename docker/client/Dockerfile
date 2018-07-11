FROM alpine:3.7

WORKDIR /root

RUN apk add --no-cache \
    git mesa-gl glu \
    python3 py3-numpy && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    pip install --trusted-host pypi.python.org \
    pyglet \
    git+https://github.com/wbap/oculoenv && \
    rm -r /root/.cache 
