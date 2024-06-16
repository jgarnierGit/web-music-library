/**
 * Filesystem description
 */
interface Folder {
    id: string,
    path: string,
    name: string,
    folders: Folder[],
    musics: Music[]
}

interface Music {
    id: string,
    path: string,
    name: string,
    album: string,
    artist: string,
    count_played: number
}

interface Artist {
    id: string,
    name: string,
    country_name: string,
    geom: string
}

interface ArtistList {
    artists: Artist[]
}

interface ArtistMapEditorContext {
    value: any;
    artist: Artist,
    callback: Function
}

export type { Folder, Music, Artist, ArtistList, ArtistMapEditorContext }