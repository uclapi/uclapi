const dotenv = require(`dotenv`)
dotenv.config({
  path: `../backend/uclapi/.env`,
})

const webpack = require(`webpack`)
const path = require(`path`)
const TerserPlugin = require(`terser-webpack-plugin`)
const OptimizeCSSAssetsPlugin = require(`optimize-css-assets-webpack-plugin`)
const BundleTracker = require(`webpack-bundle-tracker`)

const os = require(`os`)

const entryPointsPathPrefix = `./src/pages`

const {
  AWS_S3_STATICS,
  AWS_S3_BUCKET_NAME,
  AWS_S3_BUCKET_PATH,
} = process.env

const publicPath = AWS_S3_STATICS === `True`
  ? `https://${AWS_S3_BUCKET_NAME}.s3.amazonaws.com/${AWS_S3_BUCKET_PATH}`
  : `/static/`

const envKeys = Object.keys(process.env).reduce((prev, next) => {
  prev[`process.env.${next}`] = JSON.stringify(process.env[next])
  return prev
}, {})

module.exports = {
  mode: `production`,
  optimization: {
    minimize: true,
    minimizer: [],  // This list is built below as per platform requirements
    splitChunks: {
      name: false,
      cacheGroups: {
        vendors: {
          chunks: `all`,
          name: `vendors`,
          test: /[\\/]node_modules[\\/]/,
        },
      },
    },
  },
  plugins: [
    new webpack.DefinePlugin(envKeys),
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(`production`),
    }),
    new BundleTracker({
      filename: `../backend/uclapi/static/webpack-stats.json`,
    }),
    new webpack.HashedModuleIdsPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: `babel-loader`,
        },
      },
      {
        test: /\.scss|css$/,
        use: [
          { loader: `style-loader` },
          { loader: `css-loader` },
          { loader: `sass-loader` },
        ],
      },
      {
        test: /\.(jpg|png|svg|jpeg)$/,
        loader: `url-loader`,
      },
    ],
  },
  resolve: {
    alias: {
      'Images': path.resolve(__dirname, `./src/images`),
      'Layout': path.resolve(__dirname, `./src/components/layout`),
      'Dashboard': path.resolve(__dirname, `./src/components/dashboard`),
      'Styles': path.resolve(__dirname, `./src/sass`),
    },
  },
  entry: {
    index: entryPointsPathPrefix + `/HomePage.jsx`,
    documentation: entryPointsPathPrefix + `/Documentation.jsx`,
    about: entryPointsPathPrefix + `/AboutPage.jsx`,
    dashboard: entryPointsPathPrefix + `/Dashboard.jsx`,
    marketplace: entryPointsPathPrefix + `/Marketplace.jsx`,
    authorise: entryPointsPathPrefix + `/Authorise.jsx`,
    warning: entryPointsPathPrefix + `/Warning.jsx`,
    settings: entryPointsPathPrefix + `/AppSettings.jsx`,
    vendors: [`react`],
  },
  output: {
    path: path.resolve(__dirname, `../backend/uclapi/static/`),
    publicPath,
    filename: `[name]-[contenthash].js`,
  },
}

// Do not enable parallelisation for Windows Subsystem for Linux
// https://github.com/webpack-contrib/uglifyjs-webpack-plugin/issues/302
// https://stackoverflow.com/a/44356310/5297057
if (os.platform() == `linux` && os.release().indexOf(`Microsoft`) != -1) {
  module.exports.optimization.minimizer.push(
    new TerserPlugin({
      cache: true,
      sourceMap: true,
    })
  )
} else {
  module.exports.optimization.minimizer.push(
    new TerserPlugin({
      cache: true,
      sourceMap: true,
      parallel: true,
    })
  )
}
module.exports.optimization.minimizer.push(
  new OptimizeCSSAssetsPlugin({})
)
