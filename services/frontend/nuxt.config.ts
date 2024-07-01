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
  css: ['leaflet.markercluster/dist/MarkerCluster.css', 'leaflet.markercluster/dist/MarkerCluster.Default.css'],
  ssr: false,
  srcDir: 'src',
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
    // tauri config
    server: {
      strictPort: true,
      watch: {
        // 3. tell vite to ignore watching `src-tauri`
        ignored: ["**/src-tauri/**"],
      },
      hmr: {
        protocol: 'ws'
      }
    },
  },
  routeRules: {
    '/': { prerender: true }
  },
  // end tauri config
  // projectM config
  nitro: {
    experimental: {
      wasm: true
    }
  },
})