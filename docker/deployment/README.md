# UCLAPI on Docker
*WOOOHOOOOO!*

This has been a long time coming, and it has had a number of false starts, so please bear with us whilst we iron out bugs in this stack!

2021-08-31: Moved from uclapi/docker to uclapi/uclapi

## Folder Structure
### `/uclapi/`
The `uclapi` directory contains public configuration files for the main UCL API container. As with the `nginx` directory, the `supervisor-conf` directory contains the main configuration for Supervisor itself, but we also supply configuration to run the API under Gunicorn as well as a Celery worker.

We also supply a `run.sh` file as with `nginx` that watches Supervisor and brings any failed processes back online.

### `/non-public/`
This contains private configuration files we can't make public for security reasons. It is structured as follows:
```
/non-public
|-- /prod
    |-- /uclapi
        |-- uclapi.env
        |-- uclfw.rules
|-- /staging
    |-- /uclapi
        |-- uclapi.env
        |-- uclfw.rules

```
The basic structure is that within `non-public` is each environment. At the moment, we only support our `staging` and `prod` environments using this deployment stack.

Each environment has a `uclapi` folder. Within this are two files: `uclfw.rules`, which is a text file we append to `/etc/hosts` on each UCL API box to enable a connection to Oracle at UCL, and `uclapi.env` which is the `.env` file we copy to `/web/uclapi/backend/uclapi/.env` before the container is started. It contains the necessary credentials, paths and connection strings to boot the API.

## Docker
### `.env`
The settings for the environment that is built (e.g. either `staging` or `prod`) are set in this file. It is read by Docker Compose when the stack is brought online.

### `docker-compose.yml`
This is the meta Docker Compose configuration that sets all the below containers up with a series of customisable arguments.

### `uclapi.Dockerfile`
This is the main UCL API Dockerfile that sets up the API and Celery. It is designed to be stateless and scalable.

Like with our Nginx Dockerfile, it's full of hacks galore, and mainly to get Oracle working within the Container. The list of tasks it performs are as follows:

- Writes the `uclfw.rules` file to the end of `/etc/hosts` so that the API can find Oracle at UCL.
- Installs the necessary packages for the API to function.
- Installs the Oracle Instant Client and Instant Client SDK.
- Adds `ORACLE_HOME` to the container's system-wide environment.
- Adds `ORACLE_HOME` to `ld.so.conf.d` so that the libraries can be found by the system when needed.
- Symlinks the main Oracle library files so that they can be found by the system.
- Clones the API from Git, and optionaly switches to a requested SHA-1 revision.
- Installs `Gunicorn` and all the necessary Python 3 requirements container-wide (no Virtual Environment is used since no other apps run in the container).
- Sets up Supervisor.
- Sets up the main watch command, `run.sh`.

## Recommendations and Issues
If you experience issues with the API under this new stack, or you are a Docker whiz and you have suggestions on how to improve, please feel free to open an issue. Thanks for your help!
