const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');

var entryPointsPathPrefix = './src/pages';

module.exports = {
  plugins: [
    new BundleTracker({
      filename: '../backend/uclapi/webpack-stats.json'
    })
  ],
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
    getStarted: entryPointsPathPrefix + '/getStarted.jsx',
    documentation: entryPointsPathPrefix + '/documentation.jsx',
    dashboard: entryPointsPathPrefix + '/dashboard.jsx',
    marketplace: entryPointsPathPrefix + '/marketplace.jsx',
    authorise: entryPointsPathPrefix + '/authorise.jsx',
  },
  output: {
    path: path.resolve(__dirname, '../backend/uclapi/dashboard/static/'),
    filename: '[name].js'
  }
};
