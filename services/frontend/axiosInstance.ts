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
    const pathRegex = new RegExp(`\/api\/music\/[\da-f\-]{36}\/increment\/`);
    const musicRes = {
        name: "fake", album: "fakeAlbum", artist: "fakeArtist",
        count_played: 2
    } as Music;
    mock.onPost(/\/api\/music\/[\da-f\-]{36}\/increment/).reply(200, { result: musicRes }); // FIXME this one doesn't work.

    const response = await fetch('./mocks/folder-list.json');
    const listFolderResult = await response.json();

    mock.onPost('/api/folder/list').reply(200, listFolderResult);

    const responseArtists = await fetch('./mocks/artist-list.json');
    const listArtistsResult = await responseArtists.json();

    mock.onGet('/api/artist/list').reply(200, { artists: listArtistsResult.artists.slice(0, 10) });
    mock.onGet(/\/api\/artist\/list\?offset\=[0-9]+/).reply((config) => {
        if (!config.url) {
            return [200, { artists: [] }]
        }
        const url = new URL(API_BASE_URL + config.url);
        const offset = parseInt(url.searchParams.get('offset') || '0', 10);
        const limit = 10; // The number of items to return
        const endIndex = Math.min(offset + limit, listArtistsResult.artists.length);
        if (endIndex === offset) {
            return [200, { artists: [] }]
        }
        return [200, { artists: listArtistsResult.artists.slice(offset, endIndex) }];
    })

    mock.onPut(/\/api\/artist\/[\da-f\-]{36}/).reply(204);
    console.log("mocked everything")
}

if (!isServerRunning) {
    console.error("Server is not connected, axios endpoints disabled, use this only for frontend development, and make sure to mock the API data you need")
    await mockAxios();
}

export default axiosInstance;