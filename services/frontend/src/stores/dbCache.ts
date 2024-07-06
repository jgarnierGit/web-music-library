import type { ArtistList, Folder } from "~/commons/interfaces";
import { countRecursiveFileSystem } from "~/commons/utils";

export const useDbCacheStore = defineStore('dbCache', () => {
    const artistsData = ref();
    const folder = ref();
    const countFilesLoaded = ref(0);

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
    return { artistsData, folder, countFilesLoaded, setFolderContent, updateCountFiles, setArtistsData };
});