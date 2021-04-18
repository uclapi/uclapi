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

const publicPath = AWS_S3_STATICS === `true`
  ? `https://${AWS_S3_BUCKET_NAME}.s3.amazonaws.com/${AWS_S3_BUCKET_PATH}`
  : `/static/`

module.exports = {
  mode: `production`,
  optimization: {
    minimize: true,
    minimizer: [],  // This list is built below as per platform requirements
    moduleIds: `deterministic`,
    splitChunks: {
      chunks: `all`,
    },
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(`production`),
      'process.env.SENTRY_DSN_REACT': JSON.stringify(process.env.SENTRY_DSN_REACT),
    }),
    new BundleTracker({
      filename: `../backend/uclapi/static/webpack-stats.json`,
    }),
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: `babel-loader`,
        },
      },
      {
        test: /\.scss|css$/,
        use: [
          {loader: `style-loader`},
          {loader: `css-loader`},
          {loader: `sass-loader`},
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
    extensions: [`.js`, `.json`, `.jsx`],
  },
  entry: {
    index: entryPointsPathPrefix + `/Home`,
    documentation: entryPointsPathPrefix + `/Documentation.jsx`,
    about: entryPointsPathPrefix + `/AboutPage.jsx`,
    dashboard: entryPointsPathPrefix + `/Dashboard`,
    marketplace: entryPointsPathPrefix + `/Marketplace`,
    authorise: entryPointsPathPrefix + `/Authorise`,
    warning: entryPointsPathPrefix + `/Warning.jsx`,
    404: entryPointsPathPrefix + `/404.jsx`,
    500: entryPointsPathPrefix + `/500.jsx`,
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
    new TerserPlugin({}),
  )
} else {
  module.exports.optimization.minimizer.push(
    new TerserPlugin({
      parallel: true,
    }),
  )
}
module.exports.optimization.minimizer.push(
  new OptimizeCSSAssetsPlugin({}),
)
