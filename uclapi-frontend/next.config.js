/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // https://github.com/swagger-api/swagger-ui/issues/8245
  transpilePackages: [
    "react-syntax-highlighter",
    "swagger-client",
    "swagger-ui-react",
  ],
  images: {
    remotePatterns: [{ hostname: '*.medium.com'}]
  },
  typescript: {
    ignoreBuildErrors: true
  }
};

module.exports = nextConfig
