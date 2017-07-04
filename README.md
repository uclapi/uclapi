# uclapi [![Build Status](https://travis-ci.org/uclapi/uclapi.svg?branch=master)](https://travis-ci.org/uclapi/uclapi) [![codecov](https://codecov.io/gh/uclapi/uclapi/branch/master/graph/badge.svg)](https://codecov.io/gh/uclapi/uclapi)
UCL API Main Repository

## Setting Up and Building
This will walk you through setting yourself up a local development environment. This is different to if you want to deploy this into production, but luckily we have an internal set of installation scripts for this. Therefore, this guide will not walk you through, for example, getting Gunicorn or Nginx running. This is for simply getting an environment up that can be used to develop the API. Testing with Nginx and Gunicorn is done in staging prior to a production deployment.

### Requirements
We only support development under Linux. macOS is unofficially supported, and we have some instructions below on how to get the Oracle Instant Client working on macOS. All Windows developers can and should use Bash on Ubuntu on Windows under Windows 10 (Creators Update) for testing, as the environment is Ubuntu 16.04.2 LTS; this is exactly the distribution and version of Linux that we use on both our Staging and Production web servers.

Note that since the Creators Update (which includes 16.04.2; if you have not upgraded from Ubuntu 14 then there are tutorials online to do this) we have experienced zero issues building and running under Bash on Ubuntu on Windows.

### Install Dependencies
```
sudo apt-get -y install git curl libpq-dev libpq5 libpython3-dev \
    python3 python3-pip python3-virtualenv python-virtualenv \
    unzip virtualenv libaio1 build-essential libpcre3 \
    libpcre3-dev wget sed \
    redis-server
```

### Start Redis
```
sudo service redis-server start
```

### Set up Oracle (Linux)
```
# Oracle Version
ORACLE_VERSION=12_2
ORACLE_SO_VERSION=12.1

# Oracle Instant Client download links
ORACLE_INSTANTCLIENT_BASIC_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-basic-linux.x64-12.2.0.1.0.zip
ORACLE_INSTANTCLIENT_SDK_URL=https://s3.eu-west-2.amazonaws.com/uclapi-static/instantclient-sdk-linux.x64-12.2.0.1.0.zip

sudo mkdir /opt/oracle

rm -rf /opt/oracle/instantclient_$ORACLE_VERSION

wget -O instantclient.zip "$ORACLE_INSTANTCLIENT_BASIC_URL"
wget -O instantclientsdk.zip "$ORACLE_INSTANTCLIENT_SDK_URL"

sudo unzip -d/opt/oracle temp/instantclient.zip
sudo unzip -d/opt/oracle temp/instantclientsdk.zip

export ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION

pushd $ORACLE_HOME

sudo ln -s libclntsh.so.$ORACLE_SO_VERSION libclntsh.so
sudo ln -s libocci.so.$ORACLE_SO_VERSION libocci.so
sudo ln -s libclntshcore.so.$ORACLE_SO_VERSION libclntshcore.so

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
sudo ldconfig

# Add ORACLE_HOME to /etc/environment
grep -q -F "ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION" /etc/environment || sudo echo "ORACLE_HOME=/opt/oracle/instantclient_$ORACLE_VERSION" >> /etc/environment

# Add ld path to /etc/ld.so.conf.d
sudo echo "/opt/oracle/instantclient_$ORACLE_VERSION" > /etc/ld.so.conf.d/oracle.conf
sudo ldconfig

popd
```

### Set up Oracle (macOS)
*This is a slightly modified set of commands based on the instructions here: https://gist.github.com/thom-nic/6011715*

Go to this page: http://www.oracle.com/technetwork/topics/intel-macsoft-096467.html

Download:  
- instantclient-basic-macos.x64-12.1.0.2.0.zip
- instantclient-sdk-macos.x64-12.1.0.2.0.zip

Now in a terminal window, run:
```
cd /usr/local/lib/
mkdir share && cd share
mkdir oracle && cd oracle
tar -xzf ~/Downloads/instantclient-basic-macos.x64-12.1.0.2.0.zip
tar -xzf ~/Downloads/instantclient-sdk-macos.x64-12.1.0.2.0.zip
cd instantclient_12_1
ln -s libclntsh.dylib.12.1 libclntsh.dylib
ln -s libocci.dylib.12.1 libocci.dylib
export ORACLE_HOME=/usr/local/lib/share/oracle/instantclient_12_1
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$ORACLE_HOME
export LD_LIBRARY_PATH=LD_LIBRARY_PATH:$ORACLE_HOME
```
Note that you may have to use `sudo` for a significant number of those commands. If you work within a root shell (`sudo -s`), you will have to replace `~/Downloads` with the full path to you user downloads folder (e.g. `/Users/yournamehere/Downloads`).

There is a strange last step that is documented on [StackOverflow](http://stackoverflow.com/questions/31338916/sqlplus-remote-connection-giving-ora-21561), which will fix networking errors from Oracle.

Run: `hostname`

Then open `/etc/hosts` in your favorite text editor
Add the following line at the bottom:
`127.0.0.1 localhost localhost.localdomain hostname`
(where hostname should be replaced with the value you got when running `hostname` earlier)

To ensure that Oracle is always available, we recommend you add these three lines to `~/.profile`:
```
export ORACLE_HOME=/usr/local/lib/share/oracle/instantclient_12_1
export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$ORACLE_HOME
export LD_LIBRARY_PATH=LD_LIBRARY_PATH:$ORACLE_HOME
```

### Download the UCL API Source Code
```
git clone https://github.com/uclapi/uclapi
```

### Fetch Fake Shibboleth
```
git clone https://github.com/uclapi/fakeshibboleth
```

### Set up a virtual environment for UCL API
```
pushd uclapi/backend/uclapi
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
deactivate
popd
```

If this builds and installs then your Oracle configuration is also working. If it fails, try restarting your shell to pick up the new environment variables set up in the Oracle set up above. If that doesn't work, set `ORACLE_HOME` to the instantclient installation directory (on Linux with this guide it is `/opt/oracle/instantclient_12_2`; on macOS the path is `/usr/local/lib/share/oracle/instantclient_12_1`).

If you are on macOS and you receive `cx_Oracle` errors, try installing `cx_Oracle` separately like this:
```
env ARCHFLAGS="-arch x86_64" pip install cx_Oracle
```
Once this command completes you should be able to go ahead and try `pip install -r requirements.txt` again to fetch the rest of the dependencies. Note also that you will need the XCode command line tools installed in order to compile the Python native dependencies like `cx_Oracle`. You can get the Xcode tools by running `xcode-select --install`, and then pressing the resultant `Install` button. You can also accept the Apple Xcode licence agreement by running `sudo xcodebuild -license accept`. After this you should be able to install `cx_Oracle`. You may also need the Xcode command line tools installed to get `git` and the various Python tools installed, too. Alternatively, most of these tools can be obtained from [Homebrew](https://brew.sh) or [MacPorts](https://www.macports.org/).

### Set up a virtual environment for Fake Shibboleth
```
pushd fakeshibboleth
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
deactivate
popd
```

### Install PostgreSQL
Setting this up will vary based on your operating system. It is perfectly possible to just use the Windows version of Postgres and run it under Windows whilst running the rest of the code under Linux. If you are working on Linux or macOS directly then you should install PostgreSQL and then reset the `postgres` account password to one you know and can save in the .env later.

### Configure the environment variables in .env
Firstly, `cp uclapi/backend/uclapi/.env.example uclapi/backend/uclapi/.env`.

Now fill the following variables into `uclapi/backend/uclapi/env.`:
`SECRET_KEY`: set this to a random value generated by [Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)

```
SHIBBOLETH_ROOT=http://localhost:8001
UCLAPI_PRODUCTION=False
UCLAPI_DOMAIN=localhost:8000
UCLAPI_RUNNING_ON_AWS_ELB=False

DB_UCLAPI_NAME=uclapi_default
DB_UCLAPI_USERNAME=postgres
DB_UCLAPI_PASSWORD=YOUR_PASSWORD_HERE
DB_UCLAPI_HOST=localhost
DB_UCLAPI_PORT=5432
DB_UCLAPI_POOL_SIZE=20

DB_ROOMS_NAME=(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=DB_HOST_AT_UCL)(PORT=DATABASE_PORT_HERE)))(CONNECT_DATA=(SERVICE_NAME=THE_DATABASE_SERVICE_NAME)))
DB_ROOMS_USERNAME=UCLAPI_ORACLE_USERNAME
DB_ROOMS_PASSWORD=UCLAPI_ORACLE_PASSWORD#

DB_CACHE_NAME=uclapi_gencache
DB_CACHE_USERNAME=postgres
DB_CACHE_PASSWORD=YOUR_PASSWORD_HERE
DB_CACHE_HOST=localhost
DB_CACHE_PORT=5432
DB_CACHE_POOL_SIZE=20

ORACLE_HOME=PATH_TO_INSTANTCLIENT_INSTALL_DIRECTORY

OPBEAT_ORG_ID=
OPBEAT_APP_ID=
OPBEAT_SECRET_TOKEN=

KEEN_PROJECT_ID=
KEEN_WRITE_KEY=

SENTRY_DSN=

REDIS_UCLAPI_HOST=localhost
```

### Run Database Migrations, Create Lock and Populate Cache
**Note that the cache filling can only ever work if you are within the UCL network and have database access credentials.**
```
pushd uclapi/backend/uclapi
. venv/bin/activate
./manage.py migrate
./manage.py migrate --database gencache
./manage.py create_lock
./manage.py update_gencache
deactivate
popd
```

## Running the API Locally
Running the API locally requires two shells open: one for Fake Shibboleth and one for the API.
**Note that API requests can only ever work if you are within the UCL network and have database access credentials.**

### Start Dependencies
1. Ensure Postgres is running
2. Start Redis: `sudo service redis-server start`

### Starting Fake Shibboleth (Shell 1)
```
cd fakeshibboleth
. venv/bin/activate
./manage.py runserver localhost:8001 --noreload
```

### Starting the API (Shell 2)
```
cd uclapi/backend/uclapi
. venv/bin/activate
./manage.py runserver
```

### Give it a go!
If those commands work you should be able to navigate to `http://localhost:8000/dashboard` in your browser, which will let you log in via Fake Shibboleth running on `http://localhost:8001`. If so, then you're up and running!

## Testing
We're an amazing project, so obviously we have tests :sparkles:  
Make sure you have the requirements installed in your virtual environment, `cd` into `backend/uclapi` and then run :  
`python manage.py test --testrunner 'uclapi.custom_test_runner.NoDbTestRunner'`
