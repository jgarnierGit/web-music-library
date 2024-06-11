<template>
    <audio controls controlsList="nodownload" :src="audioPath">
        Your browser does not support the audio element.
    </audio>
</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { AUDIO_BASE_URL } from '~/commons/constants';
import { usePlaylistStore } from '~/stores/playlist';

const audioPath = ref<string>();
const playlist = usePlaylistStore();
const { currentPlaying } = storeToRefs(playlist);

onBeforeMount(() => console.log(AUDIO_BASE_URL));
watch(currentPlaying, (newVal) => {
    if (newVal) {
        console.log(AUDIO_BASE_URL);
        audioPath.value = `${AUDIO_BASE_URL}/${newVal}`;
    }
})

</script>