import type { Album, Artist, ContentList, Folder, Genre, Year } from "~/commons/interfaces";
import { countRecursiveFileSystem } from "~/commons/utils";

export const useDbCacheStore = defineStore('dbCache', () => {
    const artistsData = ref();
    const albumsData = ref();
    const genresData = ref();
    const yearsData = ref();
    const artistDataGeomOnly = ref();
    const folder = ref();
    const countFilesLoaded = ref(0);

    const countLoadedArtists = computed(() => artistsData.value ? artistsData.value.contents.length : 0)
    const countLoadedAlbums = computed(() => albumsData.value ? albumsData.value.contents.length : 0)
    const countLoadedGenres = computed(() => genresData.value ? genresData.value.contents.length : 0)
    const countLoadedYears = computed(() => yearsData.value ? yearsData.value.contents.length : 0)

    function setFolderContent(content: Folder) {
        folder.value = content;
        countFilesLoaded.value = countRecursiveFileSystem(content, 0);
    }

    function updateCountFiles() {
        countFilesLoaded.value = countRecursiveFileSystem(folder.value, 0);
    }

    function setArtistsData(contents: ContentList<Artist>) {
        artistsData.value = contents;
    }

    function setAlbumsData(contents: ContentList<Album>) {
        albumsData.value = contents;
    }
    function setGenresData(contents: ContentList<Genre>) {
        genresData.value = contents;
    }
    function setYearsData(contents: ContentList<Year>) {
        genresData.value = contents;
    }

    function setArtistDataGeomOnly(contents: ContentList<Artist>) {
        artistDataGeomOnly.value = contents;
    }

    return {
        artistsData, albumsData, genresData, yearsData, artistDataGeomOnly, folder, countFilesLoaded,
        countLoadedArtists, countLoadedAlbums, countLoadedGenres, countLoadedYears,
        setFolderContent, updateCountFiles, setArtistsData, setAlbumsData, setGenresData, setYearsData, setArtistDataGeomOnly
    };
});