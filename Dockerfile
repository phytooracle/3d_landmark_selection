FROM ubuntu:20.04

WORKDIR /opt
COPY . /opt

USER root

ARG DEBIAN_FRONTEND=noninteractive
ENV IRODS_USER=anonymous

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
                       libgl1-mesa-dev \
                       zip \
                       unzip \
                       libncurses5 \
                       libncurses5-dev \
                       libncursesw5 \
                       apt-transport-https \
                       gcc \
                       gnupg

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

#RUN wget https://github.com/phytooracle/phytooracle_data/archive/refs/heads/main.zip
RUN wget https://github.com/phytooracle/phytooracle_data/archive/refs/heads/main.zip
RUN unzip main.zip
RUN mv phytooracle_data-main/ phytooracle_data/
COPY . /opt

RUN wget https://files.renci.org/pub/irods/releases/4.1.10/ubuntu14/irods-icommands-4.1.10-ubuntu14-x86_64.deb \
    && apt-get install -y ./irods-icommands-4.1.10-ubuntu14-x86_64.deb

RUN apt-get update
RUN mkdir -p /root/.irods
RUN echo "{ \"irods_zone_name\": \"iplant\", \"irods_host\": \"data.cyverse.org\", \"irods_port\": 1247, \"irods_user_name\": \"$IRODS_USER\" }" > /root/.irods/irods_environment.json
RUN apt-get autoremove -y
RUN apt-get clean

ENTRYPOINT [ "/usr/local/bin/python3.7", "/opt/main.py" ]
