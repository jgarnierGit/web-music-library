import { API_BASE_URL } from './constants';
import MockAdapter from 'axios-mock-adapter';
import type { Artist, Music } from './interfaces';
import { axiosInstance, writeInfoLogs } from './restAPI';


export async function mockAxios() {
    var mock = new MockAdapter(axiosInstance, { delayResponse: 500 });
    mock.onGet("/api/artists/count").reply(200, { result: "1000" });
    mock.onGet("api/musics/count").reply(200, { result: "25000" });
    const musicRes = {
        name: "fake", album: "fakeAlbum", artist: { name: "fakeArtist" },
        count_played: 2
    } as Music;
    mock.onPost(/\/api\/music\/[\da-f\-]{36}\/increment/).reply(200, { result: musicRes });

    const response = await fetch('./mocks/folder-list.json');
    const listFolderResult = await response.json();

    mock.onPost('/api/folders/list').reply(200, listFolderResult);

    const responseArtists = await fetch('./mocks/artist-list.json');
    const listArtistsResult = await responseArtists.json();

    mock.onGet('/api/artists/list').reply(200, { contents: listArtistsResult.contents.slice(0, 20) });
    mock.onGet(/\/api\/artists\/list\?(limit=[0-9]+)?(&)?(offset\=[0-9]+)?/).reply((config) => {
        if (!config.url) {
            return [200, { contents: [] }]
        }
        const url = new URL(API_BASE_URL + config.url);
        const offset = parseInt(url.searchParams.get('offset') || '0', 10);
        const limit = 20;
        const endIndex = Math.min(offset + limit, listArtistsResult.contents.length);
        if (endIndex === offset) {
            return [200, { contents: [] }]
        }
        return [200, { contents: listArtistsResult.contents.slice(offset, endIndex) }];
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

    mock.onGet(/\/api\/folders\/refresh\?force=(true|false)/).reply(200, { result: "7c551693-f08b-4cd5-b77c-a85630f07939" });
    const folderRefreshContent = { "task_id": "34b60af4-e4f1-4d7a-8a01-9d2f3fb68916", "task_status": "PROGRESS", "task_result": { "current": 1000 } };
    mock.onGet(/\/api\/job\/[\da-f\-]{36}/).reply(200, folderRefreshContent);

    mock.onDelete(/\/api\/job\/[\da-f\-]{36}/).reply(204);

    mock.onGet("/api/map/getGeometries").reply(200, { contents: listArtistsResult.contents.filter((artist: Artist) => !!artist.geom) });
    writeInfoLogs("mocked everything");
}

