FROM ubuntu:20.04

WORKDIR /opt
COPY . /opt

USER root

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update -y
RUN apt-get install -y wget \
                       gdal-bin \
                       libgdal-dev \
                       libspatialindex-dev \
                       build-essential \
                       software-properties-common \
                       apt-utils \
                       libsm6 \
                       libxext6 \
                       libxrender-dev \
                       libgl1-mesa-dev

RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable
RUN apt-get update
RUN apt-get install -y python3-pyproj
RUN apt-get install -y libgdal-dev
RUN apt-get install libffi-dev
RUN apt-get install -y libbz2-dev
RUN add-apt-repository ppa:ubuntugis/ppa
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

RUN wget https://www.python.org/ftp/python/3.7.11/Python-3.7.11.tgz
RUN tar -xzf Python-3.7.11.tgz
RUN cd Python-3.7.11/ && ./configure --with-ensurepip=install && make && make install
RUN python3 -m pip install --upgrade pip

RUN apt-get update
RUN pip3 install -r /opt/requirements.txt
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN git clone https://github.com/phytooracle/phytooracle_data.git
COPY . /opt

ENTRYPOINT [ "/usr/local/bin/python3.7", "/opt/main.py" ]
