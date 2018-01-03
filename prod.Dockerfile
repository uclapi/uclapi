FROM ubuntu:xenial
RUN ["mkdir", "/web/"]
ADD . /web/uclapi
WORKDIR /web/uclapi
RUN ["bash", "/web/uclapi/scripts/setup.sh"]
RUN ["bash", "/web/uclapi/scripts/prod.sh"]
CMD ["bash", "/web/uclapi/scripts/prodrun.sh"]
