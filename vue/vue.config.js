// vue.config.js
module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://192.168.1.8:5001', // Flask 后端的地址
                changeOrigin: true,
                pathRewrite: { '^/': '' }, // 重写路径
            },
        },
    },
};