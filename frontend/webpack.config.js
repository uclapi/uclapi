const path = require('path');

var entryPointsPathPrefix = './src/react/pages';

module.exports = {
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },
  entry: {
    './../backend/uclapi/dashboard/static/js/getStarted': entryPointsPathPrefix + '/getStarted.jsx',
    './../backend/uclapi/dashboard/static/js/documentation': entryPointsPathPrefix + '/documentation.jsx',
    './../backend/uclapi/dashboard/static/js/dashboard': entryPointsPathPrefix + '/dashboard.jsx',
    './../backend/uclapi/marketplace/static/js/marketplace': entryPointsPathPrefix + '/marketplace.jsx',
    './../backend/uclapi/oauth/static/js/authorise': entryPointsPathPrefix + '/authorise.jsx',
  },
  output: {
    path: path.resolve(__dirname),
    filename: '[name].js'
  }
};
