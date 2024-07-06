import { defineStore } from "pinia";
import type { Music } from "~/commons/interfaces";
import { postAPI } from "~/commons/restAPI";

export const usePlaylistStore = defineStore('playlist', () => {
    const currentPlaying = ref<Music>();
    const filter = ref<{ type: string, targetIds: string[] }>();
    const nextSong = ref<Music>();

    const isPlaying = computed(() => !!currentPlaying.value);

    function setCurrentPlaying(music: Music) {
        currentPlaying.value = music;
    }

    async function setFilter(type: string, targetIds: string[]) {
        filter.value = { type, targetIds };
        await setRandomNextSong();
    }

    function resetFilter() {
        filter.value = undefined;
    }

    function setNextSong(music: Music) {
        nextSong.value = music;
    }

    function playNextSong() {
        currentPlaying.value = nextSong.value;
        nextSong.value = undefined;
    }

    async function setRandomNextSong() {
        let response;
        if (filter.value) {
            response = await postAPI(`/api/music/getRandom`, `get next random song with filtering ${filter.value}`, { filter_value: filter.value });
        }
        else {
            response = await postAPI(`/api/music/getRandom`, 'get next random song');
        }
        if (!response) {
            return
        }
        setNextSong(response);
    }

    return { currentPlaying, isPlaying, filter, nextSong, setCurrentPlaying, setFilter, playNextSong, setNextSong, setRandomNextSong, resetFilter };
});