FROM ubuntu:18.04

WORKDIR /opt
RUN mkdir /opt/3d_landmark_selection
COPY . /opt/3d_landmark_selection/

USER root

ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=3.7.11
# ARG PYTHON_VERSION=3.10.6
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

# Download and extract Python sources
RUN cd /opt \
    && wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \                                              
    && tar xzf Python-${PYTHON_VERSION}.tgz

# Build Python and remove left-over sources
RUN cd /opt/Python-${PYTHON_VERSION} \ 
    && ./configure --enable-optimizations --with-ensurepip=install \
    && make install \
    && rm /opt/Python-${PYTHON_VERSION}.tgz /opt/Python-${PYTHON_VERSION} -rf

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install -r /opt/requirements.txt
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

RUN wget https://github.com/phytooracle/phytooracle_data/archive/refs/heads/main.zip
RUN unzip main.zip
RUN mv phytooracle_data-main/ phytooracle_data/
COPY . /opt

# Install iRODS
ARG PY_UR='python3-urllib3_1.26.9-1_all.deb'
ARG LI_SS='libssl1.1_1.1.1f-1ubuntu2.16_amd64.deb'
ARG PY_RE='python3-requests_2.25.1+dfsg-2_all.deb'
ARG LSB_RELEASE="bionic" 

RUN wget -qO - https://packages.irods.org/irods-signing-key.asc | apt-key add -
RUN echo "deb [arch=amd64] https://packages.irods.org/apt/ ${LSB_RELEASE}  main" \
     tee /etc/apt/sources.list.d/renci-irods.list

RUN apt-get update
RUN wget -c \
  http://security.ubuntu.com/ubuntu/pool/main/p/python-urllib3/${PY_UR} \
  http://security.ubuntu.com/ubuntu/pool/main/o/openssl/${LI_SS} \
  http://security.ubuntu.com/ubuntu/pool/main/r/requests/${PY_RE}
RUN apt install -y --allow-downgrades \
  ./${PY_UR} \
  ./${LI_SS} \
  ./${PY_RE}
RUN rm -rf \
  ./${PY_UR} \
  ./${LI_SS} \
  ./${PY_RE}

RUN wget https://files.renci.org/pub/irods/releases/4.1.10/ubuntu14/irods-icommands-4.1.10-ubuntu14-x86_64.deb \
    && apt-get install -y ./irods-icommands-4.1.10-ubuntu14-x86_64.deb
# RUN apt install -y irods-icommands
RUN mkdir -p /root/.irods
RUN echo "{ \"irods_zone_name\": \"iplant\", \"irods_host\": \"data.cyverse.org\", \"irods_port\": 1247, \"irods_user_name\": \"$IRODS_USER\" }" > /root/.irods/irods_environment.json
RUN apt-get autoremove -y
RUN apt-get clean

ENTRYPOINT [ "/usr/local/bin/python3.7", "/opt/main.py" ]
