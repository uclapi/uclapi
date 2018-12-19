const webpack = require('webpack');
const path = require('path');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const os = require('os');

var entryPointsPathPrefix = './src/pages';

module.exports = {
  optimization: {
    minimizer: []  // This list is built below as per platform requirements
  },
  plugins: [
    new UglifyJsPlugin({
      sourceMap: true
    }),
    new webpack.DefinePlugin({
     'process.env.NODE_ENV': JSON.stringify('production')
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

// Do not enable parallelisation for Windows Subsystem for Linux
// https://github.com/webpack-contrib/uglifyjs-webpack-plugin/issues/302
// https://stackoverflow.com/a/44356310/5297057
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
module.exports.optimization.minimizer.push(
  new OptimizeCSSAssetsPlugin({})
);
