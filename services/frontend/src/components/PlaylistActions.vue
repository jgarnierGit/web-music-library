<template>
    <v-btn :icon="mdiPlay" @click="playFilter()" variant="plain" density="compact"></v-btn>
    <v-btn :disabled="isFilterActive" :icon="mdiFastForward" @click="setFilter()" density="compact"
        variant="plain"></v-btn>
</template>

<script setup lang="ts">
import { mdiFastForward, mdiPlay } from '@mdi/js';
const playlist = usePlaylistStore();
const { filter } = storeToRefs(playlist);
const props = defineProps<{
    type: string, value: string
}>();
const isFilterActive = computed(() => filter.value?.targetIds.includes(props.value));

function setFilter() {
    playlist.setFilter(props.type, [props.value]);
}

async function playFilter() {
    await playlist.setFilter(props.type, [props.value]);
    playlist.playNextSong();
}

</script>