const webpack = require('webpack');
const path = require('path');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const os = require('os');

var entryPointsPathPrefix = './src/pages';

module.exports = {
  mode: 'production',
  optimization: {
    minimizer: [],  // This list is built below as per platform requirements
    splitChunks: {
      name: false,
      cacheGroups: {
        vendors: {
          chunks: 'all',
          name: 'vendors',
          test: /[\\/]node_modules[\\/]/,
        },
      },
    },
  },
  plugins: [
    new UglifyJsPlugin({
      sourceMap: true
    }),
    new webpack.DefinePlugin({
     'process.env.NODE_ENV': JSON.stringify('production')
    }),
    new MiniCssExtractPlugin({
      filename: "[name]-[contenthash].css",
      chunkFilename: "[id]-[contenthash].css"
    }),
    new BundleTracker({
      filename: '../backend/uclapi/webpack-stats.json'
    }),
    new webpack.HashedModuleIdsPlugin()
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
          MiniCssExtractPlugin.loader,
          { loader: "css-loader" },
          { loader: "sass-loader" }
        ]
      },
      {
        test: /\.(jpg|png|svg)$/,
        loader: 'file-loader'
      },
    ]
  },
  entry: {
    getStarted: entryPointsPathPrefix + '/getStarted.jsx',
    documentation: entryPointsPathPrefix + '/documentation.jsx',
    dashboard: entryPointsPathPrefix + '/dashboard.jsx',
    marketplace: entryPointsPathPrefix + '/marketplace.jsx',
    authorise: entryPointsPathPrefix + '/authorise.jsx',
    vendors: ['react'],
  },
  output: {
    path: path.resolve(__dirname, '../backend/uclapi/dashboard/static/'),
    filename: '[name]-[contenthash].js'
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
