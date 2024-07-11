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
    music: Music,
    saved: boolean
}

interface Music {
    id: string,
    path: string,
    name: string,
    album: string,
    artist: Artist,
    count_played: number
}

interface GeomData {
    id: string,
    name: string,
    geom: any,
    feature_name: string
}

interface Artist {
    id: string,
    name: string,
    geom: any,
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

interface RestAPI {
    writeErrorLogs: (log: any) => void,

    writeWarnLogs: (log: any) => void,

    writeInfoLogs: (log: any) => void,

    execGetAPI: (request: string, context: string, base_url?: string) => Promise<any>,

    execPostAPI: (request: string, context: string, playload?: any) => Promise<any>,

    execPutAPI: (request: string, context: string, playload: any) => Promise<any>,
    execDeleteAPI: (request: string, context: string, playload: any) => Promise<any>
}

export type { Folder, File, Music, Artist, ArtistList, ArtistMapEditorContext, GeomData, RestAPI }