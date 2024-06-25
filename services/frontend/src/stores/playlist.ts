import { defineStore } from "pinia";
import type { Music } from "~/commons/interfaces";

export const usePlaylistStore = defineStore('playlist', () => {
    const currentPlaying = ref<Music>();

    const isPlaying = computed(() => !!currentPlaying.value);

    function setCurrentPlaying(music: Music) {
        currentPlaying.value = music;
    }

    return { currentPlaying, isPlaying, setCurrentPlaying };
});