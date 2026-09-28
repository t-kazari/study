/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // バックエンドAPIへのプロキシ設定（CORS回避・コンテナ間通信対応）
  async rewrites() {
    const backendUrl = process.env.BACKEND_INTERNAL_URL || 'http://localhost:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
