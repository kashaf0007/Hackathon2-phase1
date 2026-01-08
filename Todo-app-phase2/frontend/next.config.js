/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    unoptimized: true,
  },
  experimental: {
    turbo: {
      enabled: false
    }
  },
  webpack: (config, { isServer }) => {
    // Ensure that the '@' alias is properly resolved by webpack
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': __dirname + '/src',
    };
    return config;
  },
};

module.exports = nextConfig;