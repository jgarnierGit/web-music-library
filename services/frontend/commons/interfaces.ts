/**
 * Filesystem description
 */
interface Folder {
    path: string,
    name: string,
    folders: Folder[],
    musics: File[],
    error: any,
    opened: boolean
}

interface File {
    error: any,
    music: Music
}

interface Music {
    id: string,
    path: string,
    name: string,
    album: string,
    artist: string,
    count_played: number
}

interface GeomData {
    name: string,
    geom: any
}

interface Artist extends GeomData {
    id: string,
    country_name: string,
}

interface ArtistList {
    artists: Artist[]
}

interface ArtistMapEditorContext {
    value: any;
    artist: Artist,
    callback: Function
}

export type { Folder, File, Music, Artist, ArtistList, ArtistMapEditorContext, GeomData }