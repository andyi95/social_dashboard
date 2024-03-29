// https://nuxt.com/docs/api/configuration/nuxt-config

import {readFileSync, existsSync} from "node:fs";

export default defineNuxtConfig({
  ssr: false,
  // devtools: { enabled: true, timeline: {enabled: true} },
    // telemetry: true,
    app:    {
        head: {
            title: 'Social Dashboard',
            meta: [
                { name: 'description', content: 'Social Dashboard with latest media info' }
            ]
        }
    },
  modules: [
      '@pinia/nuxt',
      '@nuxtjs/i18n',
  ],
    runtimeConfig: {
      public: {
          baseURL: process.env.BASE_URL || 'http://127.0.0.1:8000/api/'
      }
    },
  build: {
    transpile: ["vuetify"]
  },
    css: ['@/assets/styles/tailwind.css'],
    i18n: {
      vueI18n: '~/i18n.ts',
    },
    vite: {
    optimizeDeps: {
      include:
        process.env.NODE_ENV === 'development'
          ? ['naive-ui', 'vueuc', 'date-fns-tz/esm/formatInTimeZone']
          : []
    },
        vue: {
        script: {
            fs: {
                fileExists(file: string): boolean {return existsSync(file)
                },
                readFile(file: string): string | undefined {return readFileSync(file, 'utf-8')
                }
            }
        }
        }
  }
})
