#!/bin/bash

# assumes the following
#   - code has been checked out
#   - Python & Node have been installed
#   - running on Ubuntu
#   - is root

apt-get update && \
  apt-get install -y libaio1 unzip wget build-essential libpq-dev libpq5 && \
wget https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip && \
  wget https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip && \
  unzip instantclient-basic-linux.x64-12.2.0.1.0.zip && \
  unzip instantclient-sdk-linux.x64-12.2.0.1.0.zip && \
  cd instantclient_12_2 && \
  ln -s libclntsh.so.12.1 libclntsh.so && \
  ln -s libocci.so.12.1 libocci.so && \
  export ORACLE_HOME=$(pwd) && \
  export DYLD_LIBRARY_PATH=DYLD_LIBRARY_PATH:$ORACLE_HOME && \
  export LD_LIBRARY_PATH=LD_LIBRARY_PATH:$ORACLE_HOME && \
cd ./backend/uclapi && \
  (sed '/cx.*/d' requirements.txt | sed -e 's/^\\-e //') | xargs -n 1 pip3 install && \
  pip3 install codecov && \
  pip3 install $(cat requirements.txt | grep "cx-Oracle") && \
  cd ../.. && \
cp ./backend/uclapi/webpack-stats.sample.json ./backend/uclapi/static/webpack-stats.json && \
  cd ./frontend/ && \
  npm ci
