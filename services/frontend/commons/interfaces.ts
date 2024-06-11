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
    artist: string
}

export type { Folder, Music }