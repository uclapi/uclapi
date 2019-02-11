#!/bin/bash

# Set up the .env with the current working directory variable
rm .env
echo "PWD=`pwd`" > .env

# Copy the Python requirements into the context folder
cp `pwd`/backend/uclapi/requirements.txt docker/requirements.txt

# Bring it up
docker-compose up
