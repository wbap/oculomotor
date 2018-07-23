FROM ubuntu:xenial

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential software-properties-common cmake curl python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip install --upgrade pip setuptools && \
    pip --no-cache-dir install \
    numpy \
    flask \
    chainer \
    torch \
    torchvision \
    tensorflow

WORKDIR /tmp/build

RUN curl -LO https://github.com/opencv/opencv/archive/3.4.2.tar.gz && \
    tar zxf 3.4.2.tar.gz && cd opencv-3.4.2 && \
    mkdir build && cd build && \
    cmake -DWITH_QT=OFF -DWITH_GTK=OFF .. && make -j4 && make install
