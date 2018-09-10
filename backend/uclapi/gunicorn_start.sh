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

# Check if we are running in a container
grep -qa docker /proc/1/cgroup
# DOCKER_RESULT will be 0 if the string is found (therefore a container)
# If the result is NOT 0 (i.e. 1) then the string is NOT found, so we are
# not running in a container
DOCKER_RESULT=$?

if [ $DOCKER_RESULT -ne 0 ]; then
    # If we do not get 0 (e.g. this is a real or virtual system)
    exec sudo -u ubuntu venv/bin/gunicorn -c gunicorn_config.py uclapi.wsgi
else
    # If we DO get zero, we are running in a container
    exec venv/bin/gunicorn -c gunicorn_config.py uclapi.wsgi
fi
