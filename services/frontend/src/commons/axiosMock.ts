import { API_BASE_URL } from './constants';
import MockAdapter from 'axios-mock-adapter';
import type { Music } from './interfaces';
import { axiosInstance, writeInfoLogs } from './restAPI';


export async function mockAxios() {
    var mock = new MockAdapter(axiosInstance, { delayResponse: 500 });
    mock.onGet("/api/artist/count").reply(200, { result: "1000" });
    const musicRes = {
        name: "fake", album: "fakeAlbum", artist: { name: "fakeArtist" },
        count_played: 2
    } as Music;
    mock.onPost(/\/api\/music\/[\da-f\-]{36}\/increment/).reply(200, { result: musicRes });

    const response = await fetch('./mocks/folder-list.json');
    const listFolderResult = await response.json();

    mock.onPost('/api/folder/list').reply(200, listFolderResult);

    const responseArtists = await fetch('./mocks/artist-list.json');
    const listArtistsResult = await responseArtists.json();

    mock.onGet('/api/artist/list').reply(200, { artists: listArtistsResult.artists.slice(0, 20) });
    mock.onGet(/\/api\/artist\/list\?offset\=[0-9]+/).reply((config) => {
        if (!config.url) {
            return [200, { artists: [] }]
        }
        const url = new URL(API_BASE_URL + config.url);
        const offset = parseInt(url.searchParams.get('offset') || '0', 10);
        const limit = 20;
        const endIndex = Math.min(offset + limit, listArtistsResult.artists.length);
        if (endIndex === offset) {
            return [200, { artists: [] }]
        }
        return [200, { artists: listArtistsResult.artists.slice(offset, endIndex) }];
    })

    mock.onPut(/\/api\/artist\/[\da-f\-]{36}/).reply(204);

    mock.onGet(/\/api\/artist\/(?<artistName>[^\/]+)\/getCountry/).reply((config) => {
        if (config.url?.includes("Spencer Whitehead")) {
            // ES = ["El Salvador", "eSwatini", "Spain" ]; NI = [ "Nicaragua", "Nigeria" ]
            return [200, { result: ["ES", "NI"] }]
        } else if (config.url?.includes("Nanette Neal")) {
            return [200, { result: [] }]
        }
        // FR = ["France"]
        return [200, { result: ["FR"] }]
    });
    writeInfoLogs("mocked everything");
}

