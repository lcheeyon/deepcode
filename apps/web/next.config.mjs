/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_APP_VERSION: process.env.NEXT_PUBLIC_APP_VERSION || "0.1.0",
    NEXT_PUBLIC_DEEPGUARD_ENV: process.env.NEXT_PUBLIC_DEEPGUARD_ENV || "local",
  },
};

export default nextConfig;
