import type { Artist, Folder, GeomData } from "./interfaces";

function createGeomData(artists: Artist[]) {
    return artists.map((artist: Artist) => {
        return { id: artist.id, name: artist.country_name, geom: artist.geom, feature_name: artist.name } as GeomData;
    })
}

function countRecursiveFileSystem(content: Folder, countFiles: number) {
    countFiles += content.musics ? content.musics.length : 0;
    for (const folder of content.folders) {
        countFiles = countRecursiveFileSystem(folder, countFiles);
    }
    return countFiles;
}

export { createGeomData, countRecursiveFileSystem };