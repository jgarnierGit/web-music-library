import axios from 'axios';
import { API_BASE_URL, VUE_APP_MOCK_SERVER_ENV } from './commons/constants';

const isServerRunning = process.env.NODE_ENV === 'production' || !VUE_APP_MOCK_SERVER_ENV;

if (!isServerRunning) {
    console.error("Server is not connected, axios endpoints disabled, use this only for frontend development, and make sure to mock the API data you need")
}

const axiosInstance = axios.create({
    baseURL: isServerRunning ? API_BASE_URL : '',
});

// Add any desired interceptors, etc.

export default axiosInstance;