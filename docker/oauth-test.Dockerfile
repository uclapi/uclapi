FROM ubuntu:18.04

#################################
######## Main Parameters ########
#################################

ARG UCLAPI_CLIENT_ID
ARG UCLAPI_CLIENT_SECRET

ENV UCLAPI_CLIENT_ID ${UCLAPI_CLIENT_ID}
ENV UCLAPI_CLIENT_SECRET ${UCLAPI_CLIENT_SECRET}

ENV UCLAPI_URL http://localhost:8000
ENV TOKEN_DEBUG_ENABLED True
#################################
########### Let's go! ###########
#################################

RUN apt-get update && \
    apt-get install -y python3 \
                       python3-wheel \
                       python3-setuptools \
                       libaio1 \
                       wget \
                       git \
                       libpython3-dev \
                       build-essential \
                       libpcre3 \
                       libpcre3-dev \
                       sed \
                       locales \
                       liblz4-1 && \
    apt-get clean

# Fix up the language / encoding environment variables to stop Pip complaining later
RUN locale-gen en_GB.UTF-8
ENV LANG en_GB.UTF-8
ENV LANGUAGE en_GB:en
ENV LC_ALL en_GB.UTF-8

# Install the latest version of Pip from the repo
# Using ADD means that when the installation script changes remotely the container will
# rebuild from this stage. Otherwise, it should progress.
ADD https://bootstrap.pypa.io/get-pip.py get-pip.py
RUN python3 get-pip.py

# Invalidate the build cache using the GitHub API if there has been a new commit.
# Courtesy of https://stackoverflow.com/a/39278224
ADD https://api.github.com/repos/uclapi/django-uclapi-oauth/git/refs/heads/master version.json

RUN mkdir /web && git clone https://github.com/uclapi/django-uclapi-oauth /web/oauth

RUN pip install --no-cache-dir django requests django-dotenv

EXPOSE 8002

RUN python3 /web/oauth/apidemo/manage.py migrate

CMD python3 /web/oauth/apidemo/manage.py runserver 0.0.0.0:8002 --noreload
