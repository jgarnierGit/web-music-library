import { defineStore } from "pinia";
import type { File, Music } from "~/commons/interfaces";
import { postAPI } from "~/commons/restAPI";

export const usePlaylistStore = defineStore('playlist', () => {
    const currentPlaying = ref<File>();
    const filter = ref<{ type: string, targetIds: string[] }>();
    const nextSong = ref<File>();
    const fetchingNextSong = ref(false);

    const isPlaying = computed(() => !!currentPlaying.value);

    function setCurrentPlaying(file: File) {
        currentPlaying.value = file;
    }

    async function setFilter(type: string, targetIds: string[]) {
        filter.value = { type, targetIds };
        await setRandomNextSong();
    }

    function resetFilter() {
        filter.value = undefined;
    }

    function setNextSong(file: File) {
        nextSong.value = file;
    }

    function playNextSong() {
        currentPlaying.value = nextSong.value;
        nextSong.value = undefined;
    }

    async function setRandomNextSong() {
        fetchingNextSong.value = true;
        let response;
        if (filter.value) {
            response = await postAPI(`/api/music/getRandom`, `get next random song with filtering ${filter.value}`, { filter: filter.value });
        }
        else {
            response = await postAPI(`/api/music/getRandom`, 'get next random song');
        }
        fetchingNextSong.value = false;
        if (!response) {
            return
        }
        const f = { music: response, saved: true } as File;
        setNextSong(f);
    }

    return { currentPlaying, isPlaying, filter, nextSong, fetchingNextSong, setCurrentPlaying, setFilter, playNextSong, setNextSong, setRandomNextSong, resetFilter };
});