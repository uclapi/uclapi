FROM python:3.6-alpine

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

RUN apk update && \
    apk upgrade && \
    apk add git

# Invalidate the build cache using the GitHub API if there has been a new commit.
# Courtesy of https://stackoverflow.com/a/39278224
ADD https://api.github.com/repos/uclapi/fakeshibboleth/git/refs/heads/master version.json

RUN mkdir /web && \
    git clone https://github.com/uclapi/fakeshibboleth /web/fakeshibboleth

RUN pip install --no-cache-dir -r /web/fakeshibboleth/requirements.txt

EXPOSE 8001

CMD python3 /web/fakeshibboleth/manage.py runserver 0.0.0.0:8001 --noreload
