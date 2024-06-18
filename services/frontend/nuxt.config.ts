import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  build: {
    transpile: ['vuetify']
  },
  alias: {
    'turf': '~/node_modules/@turf/turf/dist/esm/index.js'
  },
  ssr: false,
  modules: ['@pinia/nuxt', '@nuxt/test-utils/module',
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    //...
  ],
  vite: {
    define: {
      VUE_APP_MOCK_SERVER: false
    },
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
  nitro: {
    experimental: {
      wasm: true
    }
  },
})