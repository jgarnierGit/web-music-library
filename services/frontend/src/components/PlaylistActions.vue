<template>
    <v-btn :icon="mdiPlay" @click="playFilter()" :variant="variant" :density="density"></v-btn>
    <v-btn :disabled="isFilterActive" :icon="mdiFastForward" @click="setFilter()" :density="density"
        :variant="variant"></v-btn>
</template>

<script setup lang="ts">
import { mdiFastForward, mdiPlay } from '@mdi/js';
const playlist = usePlaylistStore();
const { filter } = storeToRefs(playlist);
const props = withDefaults(defineProps<{
    type: string, value: string[], variant?: string, density?: string
}>(), { variant: "plain", density: "compact" });
const isFilterActive = computed(() => filter.value?.targetIds === props.value);

function setFilter() {
    playlist.setFilter(props.type, props.value);
}

async function playFilter() {
    await playlist.setFilter(props.type, props.value);
    playlist.playNextSong();
}

</script>