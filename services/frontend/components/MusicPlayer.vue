<template>
    <audio controls autoplay controlsList="nodownload" :src="audioPath">
        Your browser does not support the audio element.
    </audio>
</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { API_BASE_URL, AUDIO_BASE_URL } from '~/commons/constants';
import { usePlaylistStore } from '~/stores/playlist';
import axios from 'axios';

const audioPath = ref<string>();
const playlist = usePlaylistStore();
const { currentPlaying } = storeToRefs(playlist);

onBeforeMount(() => console.log(AUDIO_BASE_URL));
watch(currentPlaying, async (newVal) => {
    if (newVal) {
        audioPath.value = `${AUDIO_BASE_URL}/${newVal.path}`;
        const response = await axios.post(`${API_BASE_URL}/filesystem/music/${newVal.id}/increment/`);
        console.log(response);
    }
})

</script>