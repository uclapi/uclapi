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
        use: [
          { loader: "style-loader" },
          { loader: "css-loader" },
          { loader: "sass-loader" }
        ]
      },
      {
        test: /\.(jpg|png|svg)$/,
        loader: 'url-loader'
      },
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
