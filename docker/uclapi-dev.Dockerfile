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

ARG UCLAPI_BRANCH
ENV UCLAPI_BRANCH ${UCLAPI_BRANCH}
ARG UCLAPI_REVISION_SHA1
ENV UCLAPI_REVISION_SHA1 ${UCLAPI_REVISION_SHA1}

#################################
########### Let's go! ###########
#################################

RUN mkdir -p /opt/oracle

RUN apt-get update && \
    apt-get install -y python3.7 \
                       python3-distutils \
                       libaio1 \
                       wget \
                       git \
                       libpq-dev \
                       libpq5 \
                       libpython3.7-dev \
                       unzip \
                       build-essential \
                       libpcre3 \
                       libpcre3-dev \
                       sed \
                       locales \
                       liblz4-1 && \
    apt-get clean

# Fix up the language / encoding environment variables to stop Pip complaining later
RUN locale-gen en_GB.UTF-8
ENV LANG en_GB.UTF-8
ENV LANGUAGE en_GB:en
ENV LC_ALL en_GB.UTF-8

# Install the latest version of Pip from the repo
# Using ADD means that when the installation script changes remotely the container will
# rebuild from this stage. Otherwise, it should progress.
ADD https://bootstrap.pypa.io/get-pip.py get-pip.py
RUN python3.7 get-pip.py

# Install Oracle. This does the following:
# - Downloads and unzips the instant client
# - Downloads and unzips the instant client SDK
# - Symlinks the required library files
# - Updates the symbol cache
# - Installs the ORACLE_HOME into the system environment variables
# - Sets up ld so that future lookups for .so files will be resolvable using the Oracle directory
RUN wget -O instantclient.zip ${ORACLE_INSTANTCLIENT_BASIC_URL} && \
    unzip -d/opt/oracle instantclient.zip && \
    wget -O instantclientsdk.zip ${ORACLE_INSTANTCLIENT_SDK_URL} && \
    unzip -d/opt/oracle instantclientsdk.zip && \
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

COPY backend/uclapi/requirements.txt requirements.txt

RUN pip3.7 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD echo "Migrating Main DB"; \
    python3.7 /web/uclapi/backend/uclapi/manage.py migrate; \
    echo "Migrating Gencache DB"; \
    python3.7 /web/uclapi/backend/uclapi/manage.py migrate --database gencache; \
    echo "Running Development Environment Setup"; \
    python3.7 /web/uclapi/backend/uclapi/manage.py dev_environment_setup; \
    echo "Starting Django on Port 8000"; \
    python3.7 /web/uclapi/backend/uclapi/manage.py runserver 0.0.0.0:8000
