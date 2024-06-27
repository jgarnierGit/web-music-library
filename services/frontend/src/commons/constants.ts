const IS_PROD = process.env.NODE_ENV === 'production';

const AUDIO_BASE_URL = 'http://localhost:8081';
const API_BASE_URL = 'http://localhost:8001';
const FRONT_PUBLIC_URL = 'http://localhost:3000';
// @ts-ignore  defined in nuxt.config.ts
const VUE_APP_MOCK_SERVER_ENV = VUE_APP_MOCK_SERVER;

const SNACKBAR_TIMEOUT = 5000;

export { AUDIO_BASE_URL, API_BASE_URL, VUE_APP_MOCK_SERVER_ENV, FRONT_PUBLIC_URL, IS_PROD, SNACKBAR_TIMEOUT };