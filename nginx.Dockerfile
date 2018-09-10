FROM ubuntu:18.04

###
### Variables
###
ARG NGINX_VERSION=1.14.0

###
### Build the image
###
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install build-essential libgeoip1 libgeoip-dev libgnutls-openssl27 \
    libgnutls30 libssl-dev zlib1g zlib1g-dev shibboleth-sp2-common \
    shibboleth-sp2-utils libpcre3 libpcre3-dev geoip-bin \
    geoip-database wget sed libtool m4 autogen automake libevent-dev \
    pkg-config supervisor git && \
    apt-get clean

# Make the directories we'll need.
# Many mkdirs here to reduce intermediary containers
# - /web will take our web files
# - tmp-build is for compiling Nginx
# - /web/internal-cert will be a self-signed SSL cert (ELB doesn't care)
# - /var/run/shibboleth is for Shibboleth's socket files
# - /var/log/shibboleth is for Shibboleth's log files
RUN mkdir /web && \
    mkdir tmp-build && \
    mkdir /web/internal-cert && \
    mkdir -p /var/run/shibboleth && \
    mkdir -p /var/log/shibboleth

WORKDIR ./tmp-build

# Build Nginx with the necessary plugins (including Shibboleth)
RUN wget -O - "https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz" | tar zxvf -
RUN git clone https://github.com/nginx-shib/nginx-http-shibboleth.git http-shib && \
    git clone https://github.com/openresty/headers-more-nginx-module.git headers-more

WORKDIR ./nginx-$NGINX_VERSION
RUN ./configure --with-http_ssl_module --with-http_realip_module --with-http_geoip_module \
            --add-module=../http-shib/ --add-module=../headers-more && \
            make && \
            make install
WORKDIR ..

# Install the Favicons
RUN git clone https://github.com/uclapi/branding uclapi-branding && \
    mkdir /web/favicons && \
    cp -Rav uclapi-branding/favicons/* /web/favicons

# Clean up the temp folder
WORKDIR ..
RUN rm -rf tmp-build

# Copy in the Nginx config
COPY ./scripts/nginx/fastcgi_params         /usr/local/nginx/conf/fastcgi_params
COPY ./scripts/nginx/fastcgi.conf           /usr/local/nginx/conf/fastcgi.conf
COPY ./scripts/nginx/shib_clear_headers     /usr/local/nginx/conf/shib_clear_headers
COPY ./scripts/nginx/shib_fastcgi_params    /usr/local/nginx/conf/shib_fastcgi_params
COPY ./scripts/nginx/nginx_proxy.conf       /usr/local/nginx/conf/nginx.conf

# Create a self-signed internal cert
RUN openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /web/internal-cert/key.pem \
    -out /web/internal-cert/cert.pem -subj "/C=GB/ST=London/L=London/O=DevOps/OU=Production/CN=uclapi.com"

# Install generic Shibboleth configuration files
RUN rm -rf /etc/shibboleth/*
COPY ./scripts/shibboleth/accessError.html          /etc/shibboleth/
COPY ./scripts/shibboleth/attrChecker.html          /etc/shibboleth/
COPY ./scripts/shibboleth/attribute-map.xml         /etc/shibboleth/
COPY ./scripts/shibboleth/attribute-policy.xml      /etc/shibboleth/
COPY ./scripts/shibboleth/bindingTemplate.html      /etc/shibboleth/
COPY ./scripts/shibboleth/console.logger            /etc/shibboleth/
COPY ./scripts/shibboleth/discoveryTemplate.html    /etc/shibboleth/
COPY ./scripts/shibboleth/globalLogout.html         /etc/shibboleth/
COPY ./scripts/shibboleth/idp-ucl-metadata.xml      /etc/shibboleth/
COPY ./scripts/shibboleth/localLogout.html          /etc/shibboleth/
COPY ./scripts/shibboleth/metadataError.html        /etc/shibboleth/
COPY ./scripts/shibboleth/native.logger             /etc/shibboleth/
COPY ./scripts/shibboleth/partialLogout.html        /etc/shibboleth/
COPY ./scripts/shibboleth/postTemplate.html         /etc/shibboleth/
COPY ./scripts/shibboleth/protocols.xml             /etc/shibboleth/
COPY ./scripts/shibboleth/security-policy.xml       /etc/shibboleth/
COPY ./scripts/shibboleth/sessionError.html         /etc/shibboleth/
COPY ./scripts/shibboleth/shibd.logger              /etc/shibboleth/
COPY ./scripts/shibboleth/sslError.html             /etc/shibboleth/
COPY ./scripts/shibboleth/syslog.logger             /etc/shibboleth/
COPY ./scripts/shibboleth/upgrade.xsl               /etc/shibboleth/

# Install custom prod Shibboleth configuration files
COPY ./scripts/shibboleth/shibboleth2.prod.xml      /etc/shibboleth/shibboleth2.xml
COPY ./scripts/shibboleth/sp-cert.prod.pem          /etc/shibboleth/sp-cert.pem
COPY ./scripts/shibboleth/sp-key.prod.pem           /etc/shibboleth/sp-key.pem

# New supervisor config that uses a local port instead of a Unix socket to fix
# issues with Docker
COPY ./scripts/supervisor/supervisord.conf          /etc/supervisor/supervisord.conf
# Install Supervisor configuration files for UCL API services
COPY ./scripts/supervisor/nginx.conf                /etc/supervisor/conf.d/
COPY ./scripts/supervisor/shib.conf                 /etc/supervisor/conf.d/

# Restart Shibboleth
RUN /etc/init.d/shibd restart

# Restart Supervisor and all inner services
RUN service supervisor stop && \
    service supervisor start && \
    supervisorctl restart all && \
    supervisorctl restart all

# Now get monitoring!
COPY ./scripts/proxyrun.sh ./run.sh
CMD ["bash", "run.sh"]
