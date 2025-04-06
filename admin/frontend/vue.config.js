module.exports = {
  devServer: {
    port: 8080,
    proxy: {
      '/admin/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
} 