#!/bin/bash

# assumes the following
#   - code has been checked out
#   - Python & Node have been installed
#   - running on Ubuntu
#   - is root

# exit when any command fails
set -e

# keep track of the last executed command
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

apt-get update
apt-get install -y libaio1 unzip wget build-essential libpq-dev libpq5 sed git locales liblz4-1

export ORACLE_VERSION=12_2
export ORACLE_SO_VERSION=12.1
export ORACLE_INSTANTCLIENT_BASIC_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip
export ORACLE_INSTANTCLIENT_SDK_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip
export ORACLE_INSTALL_DIR /opt/oracle
export ORACLE_HOME ${ORACLE_INSTALL_DIR}/instantclient_${ORACLE_VERSION}

mkdir -p /opt/oracle

# wget -O instantclient.zip "$ORACLE_INSTANTCLIENT_BASIC_URL"
# wget -O instantclientsdk.zip "$ORACLE_INSTANTCLIENT_SDK_URL"

# unzip -d/opt/oracle instantclient.zip
# unzip -d/opt/oracle instantclientsdk.zip

# export ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION

# pushd $ORACLE_HOME

# ln -s libclntsh.so.$ORACLE_SO_VERSION libclntsh.so
# ln -s libocci.so.$ORACLE_SO_VERSION libocci.so
# ln -s libclntshcore.so.$ORACLE_SO_VERSION libclntshcore.so

# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
# ldconfig

# # Add ORACLE_HOME to /etc/environment
# grep -q -F "ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION" /etc/environment || echo "ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION" >> /etc/environment

# # Add ld path to /etc/ld.so.conf.d
# echo "/opt/oracle/instantclient_$ORACLE_VERSION" > /etc/ld.so.conf.d/oracle.conf
# ldconfig

# popd

# ORACLE_INSTANTCLIENT_BASIC_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip
# ORACLE_INSTANTCLIENT_SDK_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip

# apt-get update && \
#   apt-get install -y libaio1 unzip wget build-essential libpq-dev libpq5 && \
# wget https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip && \
#   wget https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip && \
#   unzip instantclient-basic-linux.x64-12.2.0.1.0.zip && \
#   unzip instantclient-sdk-linux.x64-12.2.0.1.0.zip && \
#   cd instantclient_12_2 && \
#   ln -s libclntsh.so.12.1 libclntsh.so && \
#   ln -s libocci.so.12.1 libocci.so && \
#   export ORACLE_HOME=$(pwd) && \
#   export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$ORACLE_HOME && \
#   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
#   cd .. && \
# cd ./backend/uclapi && \
#   #(sed '/cx.*/d' requirements.txt | sed -e 's/^\\-e //') | xargs -n 1 pip install && \
#   pip install -r requirements.txt && \
#   pip install codecov && \
#   pip install $(cat requirements.txt | grep "cx-Oracle") && \
#   cd ../.. && \
# cp ./backend/uclapi/webpack-stats.sample.json ./backend/uclapi/static/webpack-stats.json && \
#   cd ./frontend/ && \
#   npm ci
