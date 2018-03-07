#!/bin/bash

# Get into the script's directory
cd "$(dirname "$0")"

# We can only do this as root (le cry) because of the ldconfig stuff
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Let's-a go!
echo "***UCL API gunicorn starter***"

# Assume that the virtualenv is in the backend/uclapi folder
echo "Activating virtualenv..."
source venv/bin/activate

# Set the ORACLE_HOME variable before anything else
echo "Getting Oracle installation directory..."
export ORACLE_HOME=`cat .env | grep ORACLE_HOME | awk -F'=' '{print $2}'`

# Update the ld cache in case it's not working
echo "Updating the LD Cache..."
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
ldconfig

# Go-Go-Gadget Gunicorn!
echo "Booting gunicorn..."
exec sudo -u ubuntu venv/bin/gunicorn -c gunicorn_config.py uclapi.wsgi