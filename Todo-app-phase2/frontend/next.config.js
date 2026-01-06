/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  serverExternalPackages: ['@tanstack/react-query'],
  images: {
    unoptimized: true,
  },
  // Configure Turbopack explicitly to avoid conflicts
  turbopack: {},
};

module.exports = nextConfig;