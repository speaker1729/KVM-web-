const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
    publicPath: './',
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:5000', // Flask 后端地址
                changeOrigin: true
            }
        }
    }
})
