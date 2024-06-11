import { defineStore } from "pinia";

export const usePlaylistStore = defineStore('playlist', () => {
    const currentPlaying = ref<string>();

    const isPlaying = computed(() => !!currentPlaying.value);

    function setCurrentPlaying(path: string) {
        currentPlaying.value = path;
    }

    return { currentPlaying, isPlaying, setCurrentPlaying };
});