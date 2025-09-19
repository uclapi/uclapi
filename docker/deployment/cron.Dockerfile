FROM ubuntu:20.04

#################################
######## Main Parameters ########
#################################

ENV ORACLE_VERSION 12_2
ENV ORACLE_SO_VERSION 12.1
ENV ORACLE_INSTANTCLIENT_BASIC_URL https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip
ENV ORACLE_INSTANTCLIENT_SDK_URL https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip

ENV ORACLE_INSTALL_DIR /opt/oracle
ENV ORACLE_HOME ${ORACLE_INSTALL_DIR}/instantclient_${ORACLE_VERSION}

ARG ENVIRONMENT
ENV ENVIRONMENT ${ENVIRONMENT}

#################################
########### Let's go! ###########
#################################
RUN mkdir /web && \
    mkdir -p /opt/oracle
WORKDIR /web

COPY ./docker/deployment/non-public/${ENVIRONMENT}/uclapi/uclfw.rules /web/uclfw.rules

RUN apt-get update && \
    apt-get install -y python3 \
                       python3-wheel \
                       python3-setuptools \
                       libaio1 \
                       wget \
                       git \
                       libpq-dev \
                       libpq5 \
                       libpython3-dev \
                       unzip \
                       build-essential \
                       libpcre3 \
                       libpcre3-dev \
                       sed \
                       supervisor \
                       liblz4-1 &&\
    apt-get clean

# Fix up the language / encoding environment variables to stop Pip complaining later
RUN apt-get install locales && locale-gen en_GB.UTF-8
ENV LANG en_GB.UTF-8
ENV LANGUAGE en_GB:en
ENV LC_ALL en_GB.UTF-8

# Install the latest version of Pip from the repo
# Using ADD means that when the installation script changes remotely the container will
# rebuild from this stage. Otherwise, it should progress.
ADD https://bootstrap.pypa.io/pip/3.8/get-pip.py get-pip.py
RUN python3 get-pip.py

# Install Oracle. This does the following:
# - Downloads and unzips the instant client
# - Downloads and unzips the instant client SDK
# - Symlinks the required library files
# - Updates the symbol cache
# - Installs the ORACLE_HOME into the system environment variables
# - Sets up ld so that future lookups for .so files will be resolvable using the Oracle directory
RUN wget -nv -O instantclient.zip ${ORACLE_INSTANTCLIENT_BASIC_URL} && \
    unzip -q -d/opt/oracle instantclient.zip && \
    wget -nv -O instantclientsdk.zip ${ORACLE_INSTANTCLIENT_SDK_URL} && \
    unzip -q -d/opt/oracle instantclientsdk.zip && \
    rm instantclient.zip && \
    rm instantclientsdk.zip && \
    ln -s ${ORACLE_HOME}/libclntsh.so.$ORACLE_SO_VERSION ${ORACLE_HOME}/libclntsh.so && \
    ln -s ${ORACLE_HOME}/libocci.so.$ORACLE_SO_VERSION ${ORACLE_HOME}/libocci.so && \
    ln -s ${ORACLE_HOME}/libclntshcore.so.$ORACLE_SO_VERSION ${ORACLE_HOME}/libclntshcore.so && \
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${ORACLE_HOME} && \
    ldconfig && \
    grep -q -F "ORACLE_HOME=${ORACLE_HOME}" /etc/environment || echo "ORACLE_HOME=${ORACLE_HOME}" >> /etc/environment && \
    echo "${ORACLE_HOME}" > /etc/ld.so.conf.d/oracle.conf && \
    ldconfig

# Install the Supervisor configuration files
COPY ./docker/deployment/cron/supervisor-conf/supervisord.conf                      /etc/supervisor/supervisord.conf
COPY ./docker/deployment/cron/supervisor-conf/celery-beat-uclapi.conf               /etc/supervisor/conf.d/
COPY ./docker/deployment/cron/supervisor-conf/celery-worker-gencache-uclapi.conf    /etc/supervisor/conf.d/
COPY ./docker/deployment/cron/supervisor-conf/celery-worker-uclapi.conf             /etc/supervisor/conf.d/

# Install the run script
COPY ./docker/deployment/cron/run.sh /web/run.sh
RUN chmod +x /web/run.sh

# Install UCL API
ADD ./backend/uclapi /web/uclapi/backend/uclapi

WORKDIR /web/uclapi

# Install all the UCL API Requirements
RUN pip install --no-cache-dir -r backend/uclapi/requirements.txt

COPY ./docker/deployment/non-public/${ENVIRONMENT}/uclapi/uclapi.env /web/uclapi/backend/uclapi/.env

# Ensure Supervisor works. If we get an error here then we know something is wrong.
# If Supervisor restarts successfully and all services start then we are okay.
RUN service supervisor stop; \
    service supervisor start; \
    supervisorctl restart all

# Put the UCL firewall rules into the hosts file then run the start script.
# This is because any hosts file changes made during the build phase of the
# container will not be kept, so they must be added at start time.
# Courtesy of: https://stackoverflow.com/a/40721996

CMD cat /web/uclfw.rules >> /etc/hosts && /web/run.sh
