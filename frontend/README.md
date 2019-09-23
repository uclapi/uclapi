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
Build and watch:
``` Bash
$ npm start
```

Build for production:
``` Bash
$ npm run build
```

## View
To see the dashboard you must start the django server and fake shibboleth app (see backend readme) then navigate to [localhost:8000/dashboard](localhost:8000/dashboard). The static files are served up by the Django server.

## Things to note

## Webpack
Running `npm start` will start webpack in auto-rebuild mode where it will watch for changes and rebuild if necessary.
Running `npm run profile` will generate a `stats.json` file which can be analysed with something like [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer) to identify areas for possible optimisation

### Django templates
Because we are serving the django templates there are certain things you need to consider. To pass data from django into the react app we serialise
the data into a json string then assign it as the global variable `window.initialData` so react can acess it. To gain access to static files
we also create the `window.staticURL` global which stores the django static file base url.

Also, remember to add render statements to any new Django templates created if they require static assets.

1. At the top of the file, load `django-webpack-loader`: `{% load render_bundle from webpack_loader %}`
2. Use `{% render_bundle 'x' 'css' %}` where `x` is the name of the webpack entry point
3. Common vendor assets can be included via `{% render_bundle 'vendors' 'js' %}`. This should be done before the main application code because the main application code (probably) depends on the vendor assets (e.g. React).
4. Use `{% render_bundle 'x' 'js' %}` for JS assets

### Creating new pages
When creating new pages, you must update the `webpack.dev.js` and `webpack.prod.js` to add a new entry point. Also remember to update `backend/uclapi/webpack-stats.sample.json` which is used when Travis runs the Django unit tests.
