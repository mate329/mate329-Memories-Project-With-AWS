/** @type {import('next').NextConfig} */

module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "static.remove.bg",
      },
      {
        protocol: "https",
        hostname: "github.com",
      },
      {
        protocol: "https",
        hostname: "memoriestest-imagesbuckettest-ifvywzlnyrzg.s3.amazonaws.com",
      },
    ],
  },
};
