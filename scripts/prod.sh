#!/bin/bash
# Setup script for a production deployment


#################
### VARIABLES ###
#################

# Version of Nginx to use
NGINX_VERSION=1.13.8

###################################
### DO NOT EDIT BELOW THIS LINE ###
###################################

echo "***** BEGINNING $DOCKER_DEPLOYMENT DEPLOYMENT *****"

# Add hosts file entries if the rules file is present
if [ -e uclfw.rules ]; then
    cat uclfw.rules >> /etc/hosts
fi

# Get current working directory and save it so we can always come back
CURRENT_DIR=`pwd`

# Update everything
apt-get update
apt-get -y upgrade

# Install the requirements
apt-get -y install git liblz4-1 libpq-dev libpq5 libpython3-dev \
    libssl-dev htop python3 python3-pip python3-virtualenv python-virtualenv \
    supervisor unzip zlib1g zlib1g-dev virtualenv libaio1 build-essential libpcre3 \
    libpcre3-dev wget sed

pushd /web/uclapi/backend/uclapi
virtualenv --python=python3 venv
. venv/bin/activate
pip3 install -r requirements.txt
pip3 install gunicorn
popd

cd $CURRENT_DIR

service supervisor stop
service supervisor start

supervisorctl restart all
supervisorctl restart all

rm -rf temp

# Save space by clearing the apt cache
apt-get clean

echo "Done!"
