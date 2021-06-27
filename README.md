# UCL API ![build](https://img.shields.io/github/workflow/status/uclapi/uclapi/CI?label=build) ![staging](https://img.shields.io/github/workflow/status/uclapi/uclapi/CD?label=staging) [![codecov](https://codecov.io/gh/uclapi/uclapi/branch/master/graph/badge.svg)](https://codecov.io/gh/uclapi/uclapi)

## What is the UCL API?
UCL API started as a **student-built** platform for **student developers** to improve the **student experience** of everyone at UCL. We now also have our own end-user facing applications in addition to this, such as UCL Assistant, our rival app to UCL GO.

### Our Goal
Create a ridiculously simple, documentation first, and comprehensive API around UCL's digital services and establish an ecosystem of third party UCL apps and services that use the API.

### Interested in using it?
Find out more at our [website](https://uclapi.com)! 

### Interested in helping build it?
Read on more to find out how to setup and build the API. From here you can start writing your own changes and submitting them. See our [Contribution Guide](CONTRIBUTING.md) to learn more about how you can contribute.

## Setting Up and Building
This will walk you through setting yourself up a local development environment. This is different to if you want to deploy this into production, but luckily we have an internal set of installation scripts for this. Therefore, this guide will not walk you through, for example, getting Gunicorn or Nginx running. This is for simply getting an environment up that can be used to develop the API. Testing with Nginx and Gunicorn is done in staging prior to a production deployment.

### Requirements
We only support development under Linux. macOS is unofficially supported, and we have some instructions below on how to get the Oracle Instant Client working on macOS. All Windows developers can and should use Bash on Ubuntu on Windows under Windows 10 for testing, as the environment is Ubuntu 18.04.1 LTS; this is exactly the distribution and version of Linux that we use in both our Staging and Production environments. When installing Ubuntu for Windows Subsystem for Linux, install the 18.04 LTS release from the Windows Store. Whilst developing under Windows natively should be possible, this is untested and we do not provide instructions to do this.

Note that since the Creators Update (which includes 16.04.2; if you have not upgraded from Ubuntu 14 then there are tutorials online to do this) we have experienced zero issues building and running under Bash on Ubuntu on Windows.

### Install Dependencies
We provide this simple command to install most of the dependencies using the apt package manager (standard on ubuntu, debian etc...). If not using this package manager you will have to find the package names for your distro yourself. The base depenencies are postgres, python3, virtual environments for python, nodejs, npm, redis and some kernel modules for async and regular expressions. The rest are for making the installation easier such as git, curl, wget and sed. These allow you to follow this readme much easier.

### Mac OS

```
pip3 install virtualenv
brew install node
brew install redis
```

### Linux
```
sudo apt-get -y install git curl libpq-dev libpq5 libpython3-dev \
    python3 python3-pip python3-virtualenv python-virtualenv \
    unzip virtualenv libaio1 build-essential libpcre3 \
    libpcre3-dev wget sed \
    redis-server nodejs npm
```

Note: redhat based systems such as RHEL, Fedora or CentOS need to install ```libnsl``` aswell for oracle DB support.

### Start Redis
```
sudo service redis-server start
```

### Mac OS
```
brew services start redis
```

### Set up Oracle (Linux)
```bash
#! /bin/bash
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

sudo unzip -d/opt/oracle instantclient.zip
sudo unzip -d/opt/oracle instantclientsdk.zip

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
- instantclient-basic-macos.x64-18.1.0.0.0.zip
- instantclient-sdk-macos.x64-18.1.0.0.0-2.zip

Now in a terminal window, run:
```
cd /usr/local/lib/
mkdir share && cd share
mkdir oracle && cd oracle
tar -xzf ~/Downloads/instantclient-basic-macos.x64-18.1.0.0.0.zip
tar -xzf ~/Downloads/instantclient-sdk-macos.x64-18.1.0.0.0-2.zip
cd instantclient_12_1
mkdir lib
```
At this stage you need to move every file from 'instantclient_12_1' folder into 'lib'. Then, you need to quarantine these files (due to gatekeeper protection system in Catalina - Follow issue on [Github](https://github.com/oracle/python-cx_Oracle/issues/341)) 

```
sudo xattr -d com.apple.quarantine *.dylib.*
```
Reinitialize your terminal window and then, run:
```
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

### Quick Note on using virtual environments

Virtual environments allow us to easily switch between Python versions and the pip packages we have installed. They are entered with the following commands:

```
Linux: . venv/bin/activate
Windows: \venv\Scripts\activate
```

You can tell you're in one by the first letters of a terminal/cmd prompt. The line should start with the name of your virtual environment for example:

```
(venv)Your-Computer:your_project UserName$
```

Once activated anything we execute will run with this environment's version of python and the versions of any packages installed within it. This must be done whenever using our project and so before running *manage.py* or other python files remember to activate the virtual environment.

Finally to exit/deactivate the virtual environment you simply type:

```
deactivate
```

### Set up a virtual environment for UCL API

The following commands enter the uclapi back-end directory, creates a virtual environment with python 3, activates it and then installs all the requirements then returns to the working directory.

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

The following terminal commands do the same as the commands in the above section just repeated in another directory.

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

An example guide for this for ubuntu is found [Here](https://tecadmin.net/install-postgresql-server-on-ubuntu/)

#### Create the required tables

Now we have PostgreSQL installed we can create some empty databases so we can complete the migrations later. There are two required, uclapi_default, and uclapi_gencache if you are using the environment variables below. These can be created by accessing the postgreSQL command prompt with the command ```psql``` and then running ```create database uclapi_default;``` and then ```create database uclapi_gencache;```

### Configure the environment variables in .env
Firstly, `cp uclapi/backend/uclapi/.env.example uclapi/backend/uclapi/.env`.

Now fill the following variables into `uclapi/backend/uclapi/env.`:
`SECRET_KEY`: set this to a random value generated by [Django Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)
**Note: if you want fakeshibboleth to login automatically follow our guide on the wiki [Auto Login FakeShibboleth](https://github.com/uclapi/uclapi/wiki/Auto-Login-FakeShibboleth)**
```
SHIBBOLETH_ROOT=http://localhost:8001
UCLAPI_PRODUCTION=False
UCLAPI_DOMAIN=localhost
UCLAPI_RUNNING_ON_AWS_ELB=False
FORBIDDEN_CALLBACK_URLS=uclapi.com;staging.ninja

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

KEEN_PROJECT_ID=
KEEN_WRITE_KEY=

SENTRY_DSN=

REDIS_UCLAPI_HOST=localhost

STATIC_URL=/static/
AWS_S3_STATICS=False
EVENTLET_NOPATCH=True
```

### Run Database Migrations, Create Lock and Populate Cache
**Note that the cache filling can only ever work if you are within the UCL network and have database access credentials. Note also that it is normal for updating the timetable cache to take a while about 5-10 minutes.**

```
pushd uclapi/backend/uclapi
. venv/bin/activate
./manage.py migrate
./manage.py migrate --database gencache
./manage.py create_lock
./manage.py update_gencache
./manage.py feed_occupeye_cache
deactivate
popd
```

### Installing Front-End npm Packages
To install these you simply run the command ```npm install``` in the ```uclapi/frontend``` directory! More details can be found [here](frontend/README.md)

## Running the API Locally
Running the API locally requires two shells open: one for Fake Shibboleth and one for the API
**Note that API requests can only ever work if you are within the UCL network and have database access credentials.**

### Start Dependencies
1. Ensure Postgres is running
2. Start Redis: `sudo service redis-server start`
3. Ensure the front end is built ``` cd uclapi/frontend && npm run build ```

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
Make sure you have the requirements installed in your virtual environment (and you have activated it) , `cd` into `backend/uclapi` and then run :  
`python manage.py test --settings=uclapi.settings_mocked`

## Commit Message

Please follow the commit message format found in `.github/.gitmessage`, we recommend you set this as your commit message template with `git config commit.template ./.github/.gitmessage`. Please use the following format (summary is the first line and is limited to 50 characters, ):
```
Summary format:
     area subarea: message (all lowercase)
Summary examples:
     backend search: add new search function
  or backend workspaces: add historical endpoint
  or frontend pages: fix 404 page location
  or github actions: refactor CI

Use the following verbs:
  add = Create a capability e.g. feature, test, dependency.
  drop = Delete a capability e.g. feature, test, dependency.
  fix = Fix an issue e.g. bug, typo, accident, misstatement.
  bump = Increase the version of something e.g. a dependency.
  make = Change the build process, or tools, or infrastructure.
  start = Begin doing something; e.g. enable a toggle, feature flag, etc.
  stop = End doing something; e.g. disable a toggle, feature flag, etc.
  optimize = A change that MUST be just about performance, e.g. speed up code.
  document = A change that MUST be only in the documentation, e.g. help files.
  refactor = A change that MUST be just refactoring.
  reformat = A change that MUST be just format, e.g. indent line, trim space, etc.
  rephrase = A change that MUST be just textual, e.g. edit a comment, doc, etc.
```

## Linting

We have a pre-commit hook set up that runs [eslint](https://eslint.org/) on all staged JS files, [stylelint](https://github.com/stylelint/stylelint) on all staged scss files, and [autopep8](https://github.com/hhatto/autopep8) & [flake8](http://flake8.pycqa.org/en/latest/) on all staged Python files. This automatically fixes style issues and stops the commit if there are any obvious problems (e.g. failure to define variable).

## Our Custom Django Management Commands
What's that?! You want even more info? This section details any custom management commands we have created for django. You can view the full list of commands including the standard ones by running the command ```python manage.py --help``` and get more information on specific commands by running ```python manage.py command --help```. The most useful commands for development are listed below in addition to this however.

### Triggering Webhooks Manually
To trigger webhooks and test them you can run the command ```python manage.py trigger_webhooks``` with the optional flag of ```--debug``` to print details of each response. **Note: this will require having data in the room_booking database. You will also want to have done this at least twice or else you will send hundreds of thousands of bookings to the endpoint**

### Testing the Timetable System
To test the timetables system you can run ```python manage.py test_personal_timetable```. This will prompt you for a UCL userid and then print out the corresponding timetable data in JSON format. **You will need to have populated both caches**

### Updating The Frontend
To update the blogs displayed on frontpage you can run the command ```python manage.py update_medium```. This will retrieve a number of articles from our blog and insert them into the front-end. The amount retrieved is set in settings.py with the varibale `MEDIUM_ARTICLE_QUANTITY` **Note: the front end does not require rebuilding after this**

### Database Updating Commands
These were covered above but for completeness you have at your disposal the following commands to set up a database lock and then update the cached data from Oracle. We also provide two caching commands for the OccupEye study space sensor data. The mini OccupEye cache only caches a small subset of data (e.g. current sensor states) while the standard cache command caches everything. In prod the mini cache operation is run every 2 mins (and takes approx. 15-20s) while the full one is run every day at 2 AM (and takes approx. 2-3 minutes).
```
python manage.py create_lock
python manage.py update_gencache
python manage.py feed_occupeye_cache
python manage.py feed_occupeye_cache_mini
```
**Note: As said previously these require valid credentials and for you to be on the UCL network to use**

## Developing using docker

### Installation of Docker

If you're using Windows, this section assumes you're using [WSL 2](https://docs.microsoft.com/en-us/windows/wsl/compare-versions) with the latest [Docker for Windows installed](https://docs.docker.com/docker-for-windows/). Make sure to have an installation of Windows 10 Education ([free licence through UCL](https://www.ucl.ac.uk/isd/services/software-hardware/software-general-information/microsoft/microsoft-software-available)).

### Cloning the repository

Download the uclapi source into a common source folder on your computer using (if using Windows, make sure you're cloning this inside WSL2, not with your Windows files):

```
git clone https://github.com/uclapi/uclapi.git
```

### Building the frontend

```
cd frontend
npm install
npm build
```

### Configure environment variables

The [docker-compose.yml](./docker-compose.yml) file will automatically override many of the environment variables set in `.env`, so you don't need to perform a lot of the updates mentioned on the rest of this page (e.g. database configs).

You will however need to update the `DB_ROOMS_*`, `SEARCH_API_*`, `PCA_LINK` and `OCCUPEYE_*` variables for a full setup. See above for more details on these variables and how to edit the `.env` file.

### Running with Docker

Start the Docker containers:

```
cd uclapi
docker-compose up -d
```

The frontend and API should now be running on port `8000` -- for example, you can see the UCL API homepage at <http://localhost:8000>.

### Updating the cache

On first run, you should update your local cache data (as detailed above, but _within_ the main UCL API Docker container).

As previously mentioned, you'll need to be connected to the UCL network and have the database credentials to be able to populate the cache.

This will take a while (potentially up to 30 minutes).

```
docker exec -it uclapi_uclapi_1 /bin/bash
cd web/uclapi/backend/uclapi
. venv/bin/activate
python3.7 manage.py create_lock
python3.7 manage.py update_gencache
python3.7 manage.py feed_occupeye_cache
deactivate
exit
```

## Documentation
As well as the user-facing documentation we also now ship our own internal Documentation
which aims to help developers contribute to our code. To make it simply run ```make html```
while in the backend directory. You can then navigate to the build directory and open up
index.html in your favourite browser to view the documentation. It can also be built in pdf, latex
and a few other formats.

