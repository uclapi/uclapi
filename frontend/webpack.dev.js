const path = require('path');

var entryPointsPathPrefix = './src/pages';

module.exports = {
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.scss$/,
        use: [{
            loader: "style-loader" // creates style nodes from JS strings
        }, {
            loader: "css-loader" // translates CSS into CommonJS
        }, {
            loader: "sass-loader" // compiles Sass to CSS
        }]
      }
    ]
  },
  entry: {
    'js/getStarted': entryPointsPathPrefix + '/getStarted.jsx',
    'js/documentation': entryPointsPathPrefix + '/documentation.jsx',
    'js/dashboard': entryPointsPathPrefix + '/dashboard.jsx',
    'js/marketplace': entryPointsPathPrefix + '/marketplace.jsx',
    'js/authorise': entryPointsPathPrefix + '/authorise.jsx',
  },
  output: {
    path: path.resolve(__dirname),
    filename: '[name].js'
  }
};
