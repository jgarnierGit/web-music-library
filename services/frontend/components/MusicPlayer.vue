<template>
    <v-row justify="center">
        <v-col>
            <audio ref="audioPlayer" controls preload="auto" autoplay="true" crossOrigin="anonymous" loop
                controlsList="nodownload" :src="audioPath" style="height:100%">
                Your browser does not support the audio element.
            </audio>
        </v-col>
        <v-col>
            <v-tooltip location="top" origin="auto" text="Change preset">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" :icon=mdiSwapHorizontal variant="text" @click="loadMilkdropPreset()" />
                </template>
            </v-tooltip>
            <v-tooltip location="top" origin="auto" text="Toggle Visualizer">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" :icon="viewerIcon" variant="text" @click="toggleViewer()" />
                </template>
            </v-tooltip>
        </v-col>
        <v-spacer />
    </v-row>

</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { API_BASE_URL, AUDIO_BASE_URL } from '~/commons/constants';
import { usePlaylistStore } from '~/stores/playlist';
import axios from 'axios';
import { mdiSwapHorizontal, mdiMonitorOff, mdiMonitor } from '@mdi/js';
const projectM = useProjectMStore();

const audioPath = ref<string>();
const playlist = usePlaylistStore();
const audioPlayer = ref();
const { currentPlaying } = storeToRefs(playlist);
const { isVisible } = storeToRefs(projectM);

audioPath.value = `/demo.mp3`;

const viewerIcon = computed(() => isVisible.value ? mdiMonitorOff : mdiMonitor)

onBeforeMount(() => console.log(AUDIO_BASE_URL));
watch(currentPlaying, async (newVal) => {
    if (newVal) {
        audioPath.value = `${AUDIO_BASE_URL}/${newVal.path}`;

        enableAudio(audioPlayer.value, false);
        try {
            const response = await axios.post(`${API_BASE_URL}/api/music/${newVal.id}/increment/`);
            console.log(response);
        } catch (err) {
            console.error(`maybe the server is stopped ${err}`)
        }

    }
})

function loadMilkdropPreset() {
    loadPreset();
}

function toggleViewer() {
    projectM.toggleMilkdrop();
}

</script>