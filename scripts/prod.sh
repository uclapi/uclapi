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

# Temp folder for bits 'n' bobs
mkdir $CURRENT_DIR/temp

# Update everything
apt-get update
apt-get -y upgrade

# Install the requirements
apt-get -y install git byobu curl libgeoip1 libgeoip-dev libgnutls-openssl27 \
    libgnutls30 libgpg-error0 libicu55 liblz4-1 libpq-dev libpq5 libpython3-dev \
    libssl-dev htop python3 python3-pip python3-virtualenv python-virtualenv \
    supervisor unzip zlib1g zlib1g-dev virtualenv libaio1 shibboleth-sp2-common \
    shibboleth-sp2-schemas shibboleth-sp2-utils build-essential libpcre3 \
    libpcre3-dev geoip-bin geoip-database wget sed libtool m4 autogen \
    automake libevent-dev pkgconf pkg-config autoconf-archive

# Set up Nginx
pushd temp
wget -O - "https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz" | tar zxvf -

# Clone the Nginx Shibboleth Module
git clone https://github.com/nginx-shib/nginx-http-shibboleth.git http-shib

# Clone the Clear Headers module
git clone https://github.com/openresty/headers-more-nginx-module.git headers-more

# Enter the Nginx folder
pushd nginx-$NGINX_VERSION

# Configure the Nginx compilation
./configure --with-http_ssl_module --with-http_realip_module --with-http_geoip_module \
            --add-module=../http-shib/ --add-module=../headers-more

# Compile Nginx
make

# Install Nginx
make install

popd
rm -rf temp/

popd

cp -Rav /web/uclapi/scripts/nginx/* /usr/local/nginx/conf/

# Create socket folder for shibboleth
mkdir /var/run/shibboleth

# Create log folder for shibboleth
mkdir /var/log/shibboleth

# Install generic Shibboleth configuration files
rm -rf /etc/shibboleth/*
cp /web/uclapi/scripts/shibboleth/accessError.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/attrChecker.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/attribute-map.xml /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/attribute-policy.xml /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/bindingTemplate.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/console.logger /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/discoveryTemplate.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/globalLogout.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/idp-ucl-metadata.xml /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/localLogout.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/metadataError.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/native.logger /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/partialLogout.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/postTemplate.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/protocols.xml /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/security-policy.xml /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/sessionError.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/shibd.logger /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/sslError.html /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/syslog.logger /etc/shibboleth/
cp /web/uclapi/scripts/shibboleth/upgrade.xsl /etc/shibboleth/

# Install custom prod/staging Shibboleth configuration files
if [ "$DOCKER_DEPLOYMENT" = "prod" ]; then
    cp /web/uclapi/scripts/shibboleth/shibboleth2.prod.xml /etc/shibboleth/shibboleth2.xml
    cp /web/uclapi/scripts/shibboleth/sp-cert.prod.pem /etc/shibboleth/sp-cert.pem
    cp /web/uclapi/scripts/shibboleth/sp-key.prod.pem /etc/shibboleth/sp-key.pem
else
    cp /web/uclapi/scripts/shibboleth/shibboleth2.staging.xml /etc/shibboleth/shibboleth2.xml
    cp /web/uclapi/scripts/shibboleth/sp-cert.staging.pem /etc/shibboleth/sp-cert.pem
    cp /web/uclapi/scripts/shibboleth/sp-key.staging.pem /etc/shibboleth/sp-key.pem
fi

# New supervisor config that uses a local port instead of a Unix socket to fix
# issues with Docker
cp /web/uclapi/scripts/supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# Install Supervisor configuration files for UCL API services
cp /web/uclapi/scripts/supervisor/celery-uclapi.conf /etc/supervisor/conf.d/
cp /web/uclapi/scripts/supervisor/gunicorn-django.conf /etc/supervisor/conf.d/
cp /web/uclapi/scripts/supervisor/nginx.conf /etc/supervisor/conf.d/
cp /web/uclapi/scripts/supervisor/shib.conf /etc/supervisor/conf.d/

# Set up Favicons from Git repo
git clone https://github.com/uclapi/branding uclapi-branding
mkdir -p /web/favicons
cp -Rav uclapi-branding/favicons/* /web/favicons
rm -rf uclapi-branding

# Generate a self-signed certificate, which is fine since we're running via ELB
# If production, we make a prod cert. Otherwise, we make one for staging.
mkdir /web/internal-cert
if [ "$DOCKER_DEPLOYMENT" = "prod" ]; then
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /web/internal-cert/key.pem -out /web/internal-cert/cert.pem -subj "/C=GB/ST=London/L=London/O=DevOps/OU=Production/CN=uclapi.com"
else
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /web/internal-cert/key.pem -out /web/internal-cert/cert.pem -subj "/C=GB/ST=London/L=London/O=DevOps/OU=Staging/CN=staging.ninja"
fi

pushd /web/uclapi/backend/uclapi
virtualenv --python=python3 venv
. venv/bin/activate
pip3 install -r requirements.txt
pip3 install gunicorn

echo yes | ./manage.py collectstatic
popd

/etc/init.d/shibd restart

cd $CURRENT_DIR

service supervisor stop
service supervisor start

supervisorctl restart all
supervisorctl restart all

rm -rf temp

echo "Done!"
