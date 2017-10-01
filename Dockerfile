FROM ubuntu:16.04
RUN ["mkdir", "uclapi"]
WORKDIR ./uclapi
ADD ./scripts/setup.sh ./scripts/setup.sh
RUN ["bash", "./scripts/setup.sh"]
CMD ["bash", "./scripts/run.sh"]
