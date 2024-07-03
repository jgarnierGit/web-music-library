import type { Artist, GeomData } from "./interfaces";

function createGeomData(artists: Artist[]) {
    return artists.map((artist: Artist) => {
        return { id: artist.id, name: artist.country_name, geom: artist.geom, feature_name: artist.name } as GeomData;
    })
}

export { createGeomData };