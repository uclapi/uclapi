# UCLAPI on Docker
*WOOOHOOOOO!*

This has been a long time coming, and it has had a number of false starts, so please bear with us whilst we iron out bugs in this stack!

2021-08-31: Moved from uclapi/docker to uclapi/uclapi

## Folder Structure
### `/nginx/`
Contains the public configuration files for the Nginx and Shibboleth container.
`nginx/nginx-conf` contains configuration files that are written straight into the Nginx directory over the top of any files with the same name already in that directory. This means that some configuration, such as the default `mime.types` file, is deliberately preserved.

`nginx/supervisor-conf` contains the following Supervisor configuration files:

- `supervisord.conf`: Main Supervisor configuration file. Installed to `/etc/supervisor/supervisord.conf`.
- `nginx.conf`: Nginx configuration for Supervisor. Installed to `/etc/supervisor/conf.d/nginx.conf`.
- `shib.conf`: Shibboleth configuration for Supervisor. This up both the `shibauthorizer` and `shibresponder` processes.

`run.sh` is the main `CMD` script for the container. It polls Supervisor to ensure that none of the processes have died. If any have, it restarts them.

### `/shibpostgres/`
We slightly tweak the default PostgreSQL installation to function as the [ODBC data backend](https://wiki.shibboleth.net/confluence/display/SP3/ODBCStorageService) for Shibboleth. The main change we make, other than to the credentials, is the injection of `shib.sql` into the `/docker-entrypoint-initdb.d/` directory, which causes it to be run on first boot. The SQL file contains the required SQL DDL to build a data structure for Shibboleth.

By storing Shibboleth's data in PostgreSQL, we are more resilient to containers crashing, getting replaced or going offline.

It may be that in production we end up pointing Shibboleth to an Amazon RDS instance instead of a containerised PostgreSQL implementation (as the lack of scaling and data replication on this database makes it a single point of failure), but for now this is acceptable.

### `/uclapi/`
The `uclapi` directory contains public configuration files for the main UCL API container. As with the `nginx` directory, the `supervisor-conf` directory contains the main configuration for Supervisor itself, but we also supply configuration to run the API under Gunicorn as well as a Celery worker.

We also supply a `run.sh` file as with `nginx` that watches Supervisor and brings any failed processes back online.

### `/non-public/`
This contains private configuration files we can't make public for security reasons. It is structured as follows:
```
/non-public
|-- /prod
    |-- /Shibboleth
        |-- sp-cert.pem
        |-- sp-key.pem
        |-- shibboleth2.xml
        |-- ...
    |-- /uclapi
        |-- uclapi.env
        |-- uclfw.rules
|-- /staging
    |-- /Shibboleth
        |-- sp-cert.pem
        |-- sp-key.pem
        |-- shibboleth2.xml
        |-- ...
    |-- /uclapi
        |-- uclapi.env
        |-- uclfw.rules
    
```
The basic structure is that within `non-public` is each environment. At the moment, we only support our `staging` and `prod` environmentss using this deployment stack.

Within each environment's directory firstly is a directory for all the Shibboleth configuration files. The deployment code performs `rm -rf /etc/shibboleth/*` prior to copying this entire directory to `/etc/shibboleth`. Unlike with Nginx, no packed configuration files are used; we replace them all with our own.

Secondly, each environment has a `uclapi` folder. Within this are two files: `uclfw.rules`, which is a text file we append to `/etc/hosts` on each UCL API box to enable a connection to Oracle at UCL, and `uclapi.env` which is the `.env` file we copy to `/web/uclapi/backend/uclapi/.env` before the container is started. It contains the necessary credentials, paths and connection strings to boot the API.

## Docker
### `.env`
The environment that is built (e.g. either `staging` or `prod`), along with the requested database credentials for Shibboleth, are set in this file. It is read by Docker Compose when the stack is brought online.

### `docker-compose.yml`
This is the meta Docker Compose configuration that sets all the below containers up with a series of customisable arguments.

### `nginx.Dockerfile`
This is the Dockerfile that brings Nginx and the Shibboleth Service Provider (SP) online. It fetches a custom-compiled version of Nginx from an S3 bucket. The actual version of Nginx expected is built using our custom-made [Nginx build container](https://github.com/uclapi/nginx-build).

Part of the setup process is generating a self-signed certificate. This is okay, because we put our environments behind an Amazon Elastic Load Balancer that has a valid SSL certificate. This again is placed behind CloudFlare which has Strict SSL enabled.

This script does a number of hacky things that are far from ideal, but we don't have a better way of doing it so far. The general list of tasks is:

- Install necessary packages for execution.
- Fetch Nginx from our S3 bucket.
- Extract Nginx to `/usr/local/nginx`
- Copy our Nginx configuration from `nginx/nginx-conf` to `/usr/local/nginx/conf`.
- Securely set up the [SWITCH](https://switch.ch) package repository so that we can get Shibboleth SP 3.x on Ubuntu 18.04.
- Install our Favicon files from our Branding repository.
- Generate a self-signed SSL Certificate.
- Install Shibboleth SP 3.x.
- Install our Shibboleth configuration from `non-public/$ENVIRONMENT/Shibboleth/` to `/etc/shibboleth`.
- Patch `shibboleth2.xml` with a connection string generated from the Postgres connection parameters in `.env`.
- Configure Supervisor.
- Set up the main watch command, `run.sh`.

### `shibpostgres.Dockerfile`
This inherits from the standard `postgres` Dockerfile, and patches in the `en_GB.UTF-8` locale. It also injects the `shib.sql` file into the entry point directory (`/docker-entrypoint-initdb.d/`) so that the necessary tables for Shibboleth are set up on first boot.

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