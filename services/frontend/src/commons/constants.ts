const IS_PROD = process.env.NODE_ENV === 'production';

const AUDIO_BASE_URL = 'http://localhost:8081';
const API_BASE_URL = 'http://localhost:8000';
const FRONT_PUBLIC_URL = IS_PROD ? 'http://tauri.localhost' : 'http://localhost:3000';
// @ts-ignore  defined in nuxt.config.ts
const VUE_APP_MOCK_SERVER_ENV = VUE_APP_MOCK_SERVER;

const SNACKBAR_TIMEOUT = 5000;

const PLAYLIST_TYPES = { ARTIST: "ARTIST", FOLDER: "FOLDER", COUNTRY: "COUNTRY" }

export { AUDIO_BASE_URL, API_BASE_URL, VUE_APP_MOCK_SERVER_ENV, FRONT_PUBLIC_URL, IS_PROD, SNACKBAR_TIMEOUT, PLAYLIST_TYPES };