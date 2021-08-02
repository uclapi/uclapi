const path = require(`path`)
const BundleTracker = require(`webpack-bundle-tracker`)
const webpack = require(`webpack`)

const entryPointsPathPrefix = `./src/pages`

const publicPath = `/static/`

module.exports = {
  mode: `development`,
  optimization: {
    minimizer: [],  // This list is built below as per platform requirements
  },
  plugins: [
    new BundleTracker({
      filename: `../backend/uclapi/static/webpack-stats.json`,
    }),
    new webpack.ProvidePlugin({
      Buffer: [`buffer`, `Buffer`], // For swagger-ui-react
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
        test: /\.(scss|css)$/,
        use: [
          { loader: `style-loader` },
          { loader: `css-loader` },
          { loader: `sass-loader` },
        ],
      },
      {
        test: /\.(jpg|png|svg|jpeg)$/,
        use: [
          {
            loader: `url-loader`,
            options: {
              esModule: false,
            },
          },
        ],
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
    documentation: entryPointsPathPrefix + `/Documentation`,
    about: entryPointsPathPrefix + `/AboutPage`,
    dashboard: entryPointsPathPrefix + `/Dashboard`,
    marketplace: entryPointsPathPrefix + `/Marketplace`,
    authorise: entryPointsPathPrefix + `/Authorise`,
    warning: entryPointsPathPrefix + `/Warning`,
    404: entryPointsPathPrefix + `/404`,
    500: entryPointsPathPrefix + `/500`,
    settings: entryPointsPathPrefix + `/AppSettings`,
    vendors: [`react`],
  },
  output: {
    path: path.resolve(__dirname, `../backend/uclapi/static/`),
    publicPath,
    filename: `[name].js`,
  },
}
