# Dashboard

This is the frontend for the uclapi.com dashboard. It is built using react and sass.

## Installation

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
To see the dashboard you must start the django server and fake shibboleth app (see backend readme) then navigate to localhost:8000/dashboard. 

## Things to note

### Django templates
Because we are serving the django templates there are certain things you need to consider. To pass data from django into the react app we serialise 
the data into a json string then assign it as the global variable `window.initialData` so react can acess it. To gain access to static files 
we also create the `window.staticURL` global which stores the django static file base url.

### Creating new pages
When you create a new page for the app you must specify which django app it is associated with. This is done in `gulp/tasks/fileModules.json`.
This file tells gulp which file goes in which django app i.e key = file name without extension, value = name of django app.
