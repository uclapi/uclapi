FROM ubuntu:xenial
RUN ["mkdir", "/web/"]
ADD . /web/uclapi
WORKDIR /web/uclapi
RUN ["bash", "/web/uclapi/scripts/setup.sh"]
CMD ["bash", "/web/uclapi/scripts/devrun.sh"]
