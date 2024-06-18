import axios from 'axios';
import { API_BASE_URL, VUE_APP_MOCK_SERVER_ENV } from './commons/constants';
import MockAdapter from 'axios-mock-adapter';
import type { Music } from './commons/interfaces';

const isServerRunning = process.env.NODE_ENV === 'production' || !VUE_APP_MOCK_SERVER_ENV;
const axiosInstance = axios.create({
    baseURL: isServerRunning ? API_BASE_URL : '',
});

if (!isServerRunning) {
    console.error("Server is not connected, axios endpoints disabled, use this only for frontend development, and make sure to mock the API data you need")
    mockAxios();
}



function mockAxios() {
    var mock = new MockAdapter(axiosInstance);
    mock.onGet("/api/artist/count").reply(200, { result: "1000" });
    const pathRegex = new RegExp(`\/api\/music\/[\da-f-]{36}\/increment\/`);
    const musicRes = {
        name: "fake", album: "fakeAlbum", artist: "fakeArtist",
        count_played: 2
    } as Music;
    mock.onPost(pathRegex).reply(200, { result: "yes" }); // FIXME this one doesn't work.
}

export default axiosInstance;