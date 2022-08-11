const {defineConfig} = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer:
        {
            host: 'localhost',
            port: 4000,
            allowedHosts: [
                'frontend',
                'localhost',
                'reader.dev.andyi95.com'
            ]
        }
})
