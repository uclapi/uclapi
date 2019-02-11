FROM ubuntu:18.04

#################################
######## Main Parameters ########
#################################

ARG AUTO_EPPN
ARG AUTO_UCLINTRANETGROUPS
ARG AUTO_CN
ARG AUTO_DEPARTMENT
ARG AUTO_GIVENNAME
ARG AUTO_DISPLAYNAME
ARG AUTO_EMPLOYEEID
ARG AUTO_AFFILIATION
ARG AUTO_MAIL
ARG AUTO_SN
ARG AUTO_UNSCOPED_AFFILIATION

ENV AUTO_EPPN ${AUTO_EPPN}
ENV AUTO_UCLINTRANETGROUPS ${AUTO_UCLINTRANETGROUPS}
ENV AUTO_CN ${AUTO_CN}
ENV AUTO_DEPARTMENT ${AUTO_DEPARTMENT}
ENV AUTO_GIVENNAME ${AUTO_GIVENNAME}
ENV AUTO_DISPLAYNAME ${AUTO_DISPLAYNAME}
ENV AUTO_EMPLOYEEID ${AUTO_EMPLOYEEID}
ENV AUTO_AFFILIATION ${AUTO_AFFILIATION}
ENV AUTO_MAIL ${AUTO_MAIL}
ENV AUTO_SN ${AUTO_SN}
ENV AUTO_UNSCOPED_AFFILIATION ${AUTO_UNSCOPED_AFFILIATION}

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
ADD https://api.github.com/repos/uclapi/fakeshibboleth/git/refs/heads/master version.json

RUN mkdir /web && git clone https://github.com/uclapi/fakeshibboleth /web/fakeshibboleth

RUN pip install --no-cache-dir -r /web/fakeshibboleth/requirements.txt

EXPOSE 8001

CMD python3 /web/fakeshibboleth/manage.py runserver 0.0.0.0:8001 --noreload
