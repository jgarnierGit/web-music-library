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

export type { Folder, Music }