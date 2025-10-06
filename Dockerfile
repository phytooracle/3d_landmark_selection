FROM ubuntu:20.04

WORKDIR /opt
COPY . /opt

USER root

ARG DEBIAN_FRONTEND=noninteractive
ENV IRODS_USER=anonymous

# Configure APT to avoid proxy caching issues
RUN echo 'Acquire::http::Pipeline-Depth "0";' > /etc/apt/apt.conf.d/99fixbadproxy && \
    echo 'Acquire::http::No-Cache "true";' >> /etc/apt/apt.conf.d/99fixbadproxy && \
    echo 'Acquire::BrokenProxy "true";' >> /etc/apt/apt.conf.d/99fixbadproxy && \
    echo 'Acquire::CompressionTypes::Order "gz";' > /etc/apt/apt.conf.d/99compression

# Clean APT cache and install system dependencies
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --fix-missing \
    python3.8 \
    python3.8-dev \
    python3-pip \
    python3-setuptools \
    python3-venv \
    wget \
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
    gnupg \
    mesa-utils \
    libgl1-mesa-glx \
    bzip2 \
    libglu1-mesa-dev \
    qt5-default \
    libnvidia-gl-440 \
    libffi-dev \
    libbz2-dev \
    libxerces-c-dev \
    libssl1.1 \
    libusb-1.0-0

# Set Python 3.8 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Add ubuntugis repository and install pyproj
RUN add-apt-repository ppa:ubuntugis/ubuntugis-unstable && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y python3-pyproj

# Set GDAL environment variables
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Install Python packages (NumPy first to avoid Open3D issues)
RUN pip install --upgrade pip wheel cython setuptools==57.5.0 numpy
RUN pip install GDAL==3.0.4
RUN pip install -r /opt/requirements.txt

# Set locale
RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'

# Download and prepare data
RUN wget https://github.com/phytooracle/phytooracle_data/archive/refs/heads/main.zip && \
    unzip main.zip && \
    mv phytooracle_data-main/ phytooracle_data/

# Install iRODS
RUN wget -qO - https://packages.irods.org/irods-signing-key.asc | apt-key add - && \
    echo "deb [arch=amd64] https://packages.irods.org/apt/ focal main" | tee /etc/apt/sources.list.d/renci-irods.list && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get upgrade -y && \
    apt install -y irods-icommands

# Configure iRODS
RUN mkdir -p /root/.irods && \
    echo "{ \"irods_zone_name\": \"iplant\", \"irods_host\": \"data.cyverse.org\", \"irods_port\": 1247, \"irods_user_name\": \"$IRODS_USER\" }" > /root/.irods/irods_environment.json

# Clean up
RUN apt-get autoremove -y && apt-get clean

ENV PYTHONPATH=/usr/local/lib/python3.8/dist-packages:$PYTHONPATH

# Entry point
ENTRYPOINT [ "python", "/opt/main.py" ]