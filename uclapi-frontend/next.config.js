/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // https://github.com/swagger-api/swagger-ui/issues/8245
  transpilePackages: [
    "react-syntax-highlighter",
    "swagger-client",
    "swagger-ui-react",
  ],
};

module.exports = nextConfig
