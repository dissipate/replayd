FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt install -y build-essential \
                   curl \
                   libcairo2-dev \
                   libffi-dev \
                   libgif-dev \
                   libjpeg-dev \
                   libssl-dev \
                   memcached \
                   pkg-config \
                   python3.7 \
                   python3.7-dev \
                   vim \
                   wait-for-it \
                   wget

ADD . /opt/replayd
ADD ./conf/config.toml /etc/replayd/config.toml
ADD ./conf/wsgi.ini /etc/replayd/wsgi.ini
RUN chown -R www-data:www-data /opt/replayd
RUN chown -R www-data:www-data /etc/replayd
WORKDIR /opt/replayd

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.7 get-pip.py
RUN pip3.7 install -r requirements.txt
