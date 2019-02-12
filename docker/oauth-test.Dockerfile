FROM python:3.6-alpine

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

RUN apk update && \
    apk upgrade && \
    apk add git

# Invalidate the build cache using the GitHub API if there has been a new commit.
# Courtesy of https://stackoverflow.com/a/39278224
ADD https://api.github.com/repos/uclapi/django-uclapi-oauth/git/refs/heads/master version.json

RUN mkdir /web && git clone https://github.com/uclapi/django-uclapi-oauth /web/oauth

RUN pip install --no-cache-dir django requests django-dotenv

EXPOSE 8002

RUN python3 /web/oauth/apidemo/manage.py migrate

CMD python3 /web/oauth/apidemo/manage.py runserver 0.0.0.0:8002 --noreload
