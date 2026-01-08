/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  webpack: (config, { isServer }) => {
    // Ensure that the 'src' alias is properly resolved by webpack
    config.resolve.alias = {
      ...config.resolve.alias,
      src: __dirname + '/src',
    };
    return config;
  },
};

module.exports = nextConfig;