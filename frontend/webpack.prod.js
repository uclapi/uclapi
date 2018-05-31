const webpack = require('webpack');
const path = require('path');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

var entryPointsPathPrefix = './src/pages';

module.exports = {
  optimization: {
    minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true // set to true if you want JS source maps
      }),
      new OptimizeCSSAssetsPlugin({})
    ]
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
