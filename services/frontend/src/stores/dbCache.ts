import type { ArtistList, Folder } from "~/commons/interfaces";
import { countRecursiveFileSystem } from "~/commons/utils";

export const useDbCacheStore = defineStore('dbCache', () => {
    const artistsData = ref();
    const artistDataGeomOnly = ref();
    const folder = ref();
    const countFilesLoaded = ref(0);

    const countLoadedArtists = computed(() => artistsData.value ? artistsData.value.artists.length : 0)

    function setFolderContent(content: Folder) {
        folder.value = content;
        countFilesLoaded.value = countRecursiveFileSystem(content, 0);
    }

    function updateCountFiles() {
        countFilesLoaded.value = countRecursiveFileSystem(folder.value, 0);
    }

    function setArtistsData(artists: ArtistList) {
        artistsData.value = artists;
    }

    function setArtistDataGeomOnly(artists: ArtistList) {
        artistDataGeomOnly.value = artists;
    }

    return {
        artistsData, artistDataGeomOnly, folder, countFilesLoaded,
        countLoadedArtists,
        setFolderContent, updateCountFiles, setArtistsData, setArtistDataGeomOnly
    };
});