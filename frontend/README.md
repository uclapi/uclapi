# Dashboard

This is the frontend for the uclapi.com dashboard. It is built using react and sass.

## Instalation

### Prerequisites 
To build the frontend you need Node.js and npm installed. 

OSX:
``` Bash
$ brew install node
```

Ubuntu/Debian:
``` Bash
$ sudo apt-get install nodejs
$ sudo apt-get install npm
$ sudo ln -s /usr/bin/nodejs /usr/bin/node # create symlink as most nodejs tools use the name node to execute
```

### Install

```
$ npm install
```

## Build
Build:
``` Bash
$ npm run build
```

Build and watch (doesn't work on windows):
``` Bash
$ npm start
```

Build for production:
``` Bash
$ npm run production
```

## View
To see the dashboard you must start the django server (see backend readme) then navigate to localhost:8000/dashboard. 
