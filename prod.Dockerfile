FROM ubuntu:18.04

# Specify whether this is a prod or staging build.
# The environment argument is used to derive a .env file to install.
ARG environment

RUN mkdir -p /web/uclapi/backend/
COPY ./backend/uclapi                           /web/uclapi/backend/uclapi

# Delete all old .env files
RUN rm -rf /web/uclapi/backend/uclapi/*.env && \
    rm -f /web/uclapi/backend/uclapi/.env

WORKDIR /web/uclapi
COPY ./scripts/uclfw.rules  uclfw.rules
COPY ./scripts/setup.sh     setup.sh
COPY ./scripts/prod.sh      prod.sh
COPY ./scripts/prodrun.sh   prodrun.sh

RUN ["bash", "/web/uclapi/setup.sh"]

# Copy our replacement config files in before Supervisor is installed
# by the setup.sh script.
# This avoids dpkg errors about pre-existing config files.
COPY ./scripts/supervisor/supervisord.conf      /etc/supervisor/supervisord.conf
COPY ./scripts/supervisor/gunicorn-django.conf  /etc/supervisor/conf.d/
COPY ./scripts/supervisor/celery-uclapi.conf    /etc/supervisor/conf.d/

RUN ["bash", "/web/uclapi/prod.sh"]

# Add in the appropriate .env file
# This is required for now because Supervisor inherits the
# environment variables from init/upstart/systemd and not
# the shell.
COPY ./backend/uclapi/${environment}.env        /web/uclapi/backend/uclapi/.env

CMD ["bash", "/web/uclapi/prodrun.sh"]
