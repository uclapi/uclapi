FROM ubuntu:20.04

#################################
#### Control versioning here ####
#################################

# Nginx build version
# latest will get the LATEST_BUILD file and download the file referenced there.
# Other values will download the tar.gz from the bucket.
ARG NGINX_BUILD
ARG ENVIRONMENT

ENV NGINX_BUILD ${NGINX_BUILD}
ENV ENVIRONMENT ${ENVIRONMENT}

ENV DEBIAN_FRONTEND="noninteractive" TZ="Europe/London"

#################################
######## Main Parameters ########
#################################
ENV AWS_BUCKET uclapi-dist

#################################
########### Let's go! ###########
#################################
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y wget \
                       curl \
                       supervisor \
                       libgeoip1 \
                       libgnutls30 \
                       zlib1g \
                       libpcre3 \
                       geoip-bin \
                       geoip-database \
                       sed \
                       git \
                       gnupg && \
    apt-get clean

# Installing Certbot
RUN apt-get install -y python3 python3-dev libffi7 libffi-dev libssl-dev curl build-essential procps && \
    curl -L 'https://bootstrap.pypa.io/get-pip.py' | python3 && \
    pip install -U cffi certbot && \
    apt-get remove --purge -y python3-dev build-essential libffi-dev libssl-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing Nginx
ENV NGINX_AWS_URL https://${AWS_BUCKET}.s3.amazonaws.com/nginx

RUN if [ "$NGINX_BUILD" = "latest" ]; \
        then export NGINX_BUILD=`curl ${NGINX_AWS_URL}/LATEST_BUILD`; \
    fi; \
    export NGINX_AWS_URL=${NGINX_AWS_URL}/${NGINX_BUILD}; \
    echo -n "Using Nginx Build: "; \
    echo ${NGINX_BUILD}; \
    echo -n "URL: "; \
    echo ${NGINX_AWS_URL}; \
    mkdir -p /usr/local/nginx && \
    wget "${NGINX_AWS_URL}" -O - | tar zxvf - -C /usr/local/nginx/

COPY ./nginx/nginx-conf/* /usr/local/nginx/conf/
RUN mkdir /usr/local/nginx/conf/conf.d
COPY ./nginx/nginx-conf/conf.d/* /usr/local/nginx/conf/conf.d/

RUN if [ ${ENVIRONMENT} = "production" ]; \
    then sed -i -e 's/SERVER_NAME_HERE/uclapi\.com/' /usr/local/nginx/conf/conf.d/nginx.conf; \
    else sed -i -e 's/SERVER_NAME_HERE/staging\.ninja/' /usr/local/nginx/conf/conf.d/nginx.conf; \
    fi

# Set up the SWITCH respository to get Shibboleth SP 3
RUN wget http://pkg.switch.ch/switchaai/SWITCHaai-swdistrib.asc && \
    VERIFY_CHECKSUM=`shasum -a 256 SWITCHaai-swdistrib.asc | head -n1 | awk '{print $1;}'` && \
    echo $VERIFY_CHECKSUM && \
    if [ "$VERIFY_CHECKSUM" != "67f733e2cdb248e96275546146ea2997b6d0c0575c9a37cb66e00d6012a51f68" ]; then exit 1; fi; \
    apt-key add SWITCHaai-swdistrib.asc && \
    rm SWITCHaai-swdistrib.asc && \
    echo 'deb http://pkg.switch.ch/switchaai/ubuntu bionic main' | tee /etc/apt/sources.list.d/SWITCHaai-swdistrib.list > /dev/null && \
    apt-get update

RUN mkdir -p /web/favicons && \
    mkdir /web/internal-cert && \
    git clone https://github.com/uclapi/branding uclapi-branding && \
    cp -Rav uclapi-branding/favicons/* /web/favicons && \
    rm -rf uclapi-branding

RUN if [ ${ENVIRONMENT} = "production" ]; \
    then openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /web/internal-cert/key.pem \
-out /web/internal-cert/cert.pem -subj "/C=GB/ST=London/L=London/O=DevOps/OU=Production/CN=uclapi.com"; \
    else openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /web/internal-cert/key.pem \
-out /web/internal-cert/cert.pem -subj "/C=GB/ST=London/L=London/O=DevOps/OU=Staging/CN=staging.ninja"; \
    fi

RUN apt-get -y install shibboleth-sp-common shibboleth-sp-utils odbc-postgresql && \
    apt-get clean && \
    rm -rf /etc/shibboleth/*

COPY ./non-public/${ENVIRONMENT}/Shibboleth/* /etc/shibboleth/

ARG POSTGRES_DATABASE
ARG POSTGRES_USERNAME
ARG POSTGRES_PASSWORD

ENV POSTGRES_DATABASE ${POSTGRES_DATABASE}
ENV POSTGRES_USERNAME ${POSTGRES_USERNAME}
ENV POSTGRES_PASSWORD ${POSTGRES_PASSWORD}

RUN echo -n "Setting up PostgreSQL Credentials with username: " && echo ${POSTGRES_USERNAME}

RUN if [ -z "${POSTGRES_USERNAME}" ]; then echo "POSTGRES VARS NOT SET"; exit 2; fi

ENV ODBC_CONNECTION_STRING Driver=/usr/lib/x86_64-linux-gnu/odbc/psqlodbca.so;Server=shibpostgres;Port=5432;Database=${POSTGRES_DATABASE};Uid=${POSTGRES_USERNAME};Password=${POSTGRES_PASSWORD}

RUN sed -i -e 's@ODBC_CONNECTION_STRING@'"${ODBC_CONNECTION_STRING}"'@' /etc/shibboleth/shibboleth2.xml

COPY ./nginx/supervisor-conf/supervisord.conf /etc/supervisor/supervisord.conf
COPY ./nginx/supervisor-conf/shib.conf        /etc/supervisor/conf.d/
COPY ./nginx/supervisor-conf/nginx.conf       /etc/supervisor/conf.d/

RUN mkdir -p /var/run/shibboleth
RUN mkdir -p /var/www/letsencrypt

COPY ./nginx/run.sh ./run.sh
COPY ./nginx/util.sh ./util.sh
COPY ./nginx/run-certbot.sh ./run-certbot.sh
RUN chmod +x ./run.sh ./util.sh ./run-certbot.sh

ARG VERSION
ENV VERSION ${VERSION}
RUN echo -n "Injecting version number: " && echo ${VERSION}
RUN sed -i -e "s/VERSION_NUMBER_HERE/${VERSION}/" /usr/local/nginx/conf/conf.d/certbot.conf
RUN sed -i -e "s/VERSION_NUMBER_HERE/${VERSION}/" /usr/local/nginx/conf/conf.d/nginx.conf

CMD ["bash", "run.sh"]
