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

sudo apt-get update && \
sudo apt-get install -y libaio1 unzip wget build-essential libpq-dev libpq5 sed git locales liblz4-1

export ORACLE_VERSION=12_2
export ORACLE_SO_VERSION=12.1
export ORACLE_INSTANTCLIENT_BASIC_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip
export ORACLE_INSTANTCLIENT_SDK_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip
export ORACLE_INSTALL_DIR=/opt/oracle
export ORACLE_HOME=${ORACLE_INSTALL_DIR}/instantclient_${ORACLE_VERSION}

sudo mkdir -p /opt/oracle

wget -O instantclient.zip "$ORACLE_INSTANTCLIENT_BASIC_URL"
wget -O instantclientsdk.zip "$ORACLE_INSTANTCLIENT_SDK_URL"

sudo unzip -d/opt/oracle instantclient.zip
sudo unzip -d/opt/oracle instantclientsdk.zip

export ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION

pushd $ORACLE_HOME

sudo ln -s libclntsh.so.$ORACLE_SO_VERSION libclntsh.so
sudo ln -s libocci.so.$ORACLE_SO_VERSION libocci.so
sudo ln -s libclntshcore.so.$ORACLE_SO_VERSION libclntshcore.so

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
sudo ldconfig

popd