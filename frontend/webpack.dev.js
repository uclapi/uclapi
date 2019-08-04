const os = require('os');
const path = require('path');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

var entryPointsPathPrefix = './src/pages';

const publicPath = '/static/';

module.exports = {
  mode: 'development',
  optimization: {
    minimizer: []  // This list is built below as per platform requirements
  },
  plugins: [
    new UglifyJsPlugin({
      sourceMap: true
    }),
    new BundleTracker({
      filename: '../backend/uclapi/static/webpack-stats.json'
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
  resolve: {
    alias: {
      'Images': path.resolve(__dirname, './src/images'),
      'Layout': path.resolve(__dirname, './src/components/layout'),
      'Styles': path.resolve(__dirname, './src/sass'),
    }
  },
  entry: {
    HomePage: entryPointsPathPrefix + '/HomePage.jsx',
    Documentation: entryPointsPathPrefix + '/Documentation.jsx',
    dashboard: entryPointsPathPrefix + '/dashboard.jsx',
    Marketplace: entryPointsPathPrefix + '/Marketplace.jsx',
    authorise: entryPointsPathPrefix + '/authorise.jsx',
    appsettings: entryPointsPathPrefix + '/appsettings.jsx',
    vendors: ['react'],
  },
  output: {
    path: path.resolve(__dirname, '../backend/uclapi/static/'),
    publicPath,
    filename: '[name].js'
  }
};
if (os.platform == "linux" && os.release().indexOf("Microsoft") != -1) {
  module.exports.optimization.minimizer.push(
    new UglifyJsPlugin({
      cache: true,
      sourceMap: true
    })
  );
} else {
  module.exports.optimization.minimizer.push(
    new UglifyJsPlugin({
      cache: true,
      sourceMap: true,
      parallel: true
    })
  );
}