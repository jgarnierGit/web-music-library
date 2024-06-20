import axios from 'axios';
import { API_BASE_URL, VUE_APP_MOCK_SERVER_ENV } from './commons/constants';
import MockAdapter from 'axios-mock-adapter';
import type { Music } from './commons/interfaces';

const isServerRunning = process.env.NODE_ENV === 'production' || !VUE_APP_MOCK_SERVER_ENV;
const axiosInstance = axios.create({
    baseURL: isServerRunning ? API_BASE_URL : '',
});

async function mockAxios() {
    var mock = new MockAdapter(axiosInstance, { delayResponse: 500 });
    mock.onGet("/api/artist/count").reply(200, { result: "1000" });
    const pathRegex = new RegExp(`\/api\/music\/[\da-f-]{36}\/increment\/`);
    const musicRes = {
        name: "fake", album: "fakeAlbum", artist: "fakeArtist",
        count_played: 2
    } as Music;
    mock.onPost(pathRegex).reply(200, { result: "yes" }); // FIXME this one doesn't work.

    const response = await fetch('./mocks/folder-list.json');
    const listFolderResult = await response.json();

    mock.onPost('/api/folder/list').reply(200, listFolderResult);

    const responseArtists = await fetch('./mocks/artist-list.json');
    const listArtistsResult = await responseArtists.json();

    mock.onGet('/api/artist/list').reply(200, listArtistsResult);
    const pathListArtistRegex = new RegExp(`api/artist\/list\?offset\=[0-9]+`);// FIXME this one doesn't work.
    mock.onGet(pathListArtistRegex).reply(200, { artists: [] })
}

if (!isServerRunning) {
    console.error("Server is not connected, axios endpoints disabled, use this only for frontend development, and make sure to mock the API data you need")
    await mockAxios();
}

export default axiosInstance;