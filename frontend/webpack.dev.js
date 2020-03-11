const path = require(`path`)
const BundleTracker = require(`webpack-bundle-tracker`)

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
        test: /\.(scss|css)$/,
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
    settings: entryPointsPathPrefix + `/AppSettings.jsx`,
    vendors: [`react`],
  },
  output: {
    path: path.resolve(__dirname, `../backend/uclapi/static/`),
    publicPath,
    filename: `[name].js`,
  },
}
