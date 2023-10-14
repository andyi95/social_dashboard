// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: true },
  modules: [
      '@pinia/nuxt',
      '@nuxtjs/i18n'
  ],
    runtimeConfig: {
      public: {
          baseURL: process.env.BASE_URL || 'http://127.0.0.1:8000/api/'
      }
    },
      build: {
        // transpile: ['vueuc'],   // fix dev error: Cannot find module 'vueuc'
        // postcss: {
        //     postcssOptions: require('./postcss.config.js')
        // }
    },
    css: ['@/assets/styles/tailwind.css'],
    i18n: {
      vueI18n: '~/i18n.ts',
    }
})
