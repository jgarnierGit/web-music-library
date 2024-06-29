<template>
    <v-row justify="center">
        <v-col>
            <audio ref="audioPlayer" controls preload="auto" autoplay="true" crossOrigin="anonymous" loop
                controlsList="nodownload" :src="audioPath" style="height:100%">
                Your browser does not support the audio element.
            </audio>
        </v-col>
        <v-col style="vertical-align: middle">
            <v-tooltip location="top" origin="auto" text="Toggle Visualizer">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" :icon="viewerIcon" variant="text" @click="toggleViewer()" />
                </template>
            </v-tooltip>
            <v-tooltip v-if="isVisible" location="top" origin="auto" text="Change preset">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" :icon=mdiSwapHorizontal variant="text" @click="loadMilkdropPreset()" />
                </template>
            </v-tooltip>
            <v-tooltip v-if="isVisible" location="top" origin="auto" :text="focusTooltip">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" :icon="viewerIconMode" variant="text" @click="toggleViewerMode()" />
                </template>
            </v-tooltip>
        </v-col>
    </v-row>

</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { AUDIO_BASE_URL, SNACKBAR_TIMEOUT } from '~/commons/constants';
import { usePlaylistStore } from '~/stores/playlist';
import { mdiSwapHorizontal, mdiMonitorOff, mdiMonitor, mdiFullscreen, mdiFullscreenExit } from '@mdi/js';
import { restAPI } from '~/commons/restAPI';
const projectM = useProjectMStore();

const audioPath = ref<string>();
const playlist = usePlaylistStore();
const snackbarStore = useSnackbarStore();
const audioPlayer = ref();
const { currentPlaying } = storeToRefs(playlist);
const { isVisible, isFocused } = storeToRefs(projectM);

// audioPath.value = `/demo.mp3`; //TODO  mock file system

const viewerIcon = computed(() => isVisible.value ? mdiMonitorOff : mdiMonitor)
const viewerIconMode = computed(() => isFocused.value ? mdiFullscreenExit : mdiFullscreen)
const focusTooltip = computed(() => isFocused.value ? "Background mode" : "Focus mode")

onMounted(() => {
    audioPlayer.value.onerror = function (err: any) {
        restAPI.writeErrorLogs(`Audio PLayer failed to read audio ${audioPath.value}, ${JSON.stringify(err)}`);
    }
})
watch(currentPlaying, async (newVal) => {
    if (newVal) {
        audioPath.value = `${AUDIO_BASE_URL}${newVal.path}`;

        restAPI.writeInfoLogs(`playing ${audioPath.value}`);
        enableAudio(audioPlayer.value, false);
        const response = await postAPI(`/api/music/${newVal.id}/increment/`, 'incrementing play count for artist');
        if (!response) {
            return
        }
        console.log(response);


    }
})

async function postAPI(request: string, context: string) {
    try {
        const getRes = await restAPI.postTauriAPI(request, context);
        if (getRes.status !== 200) {
            restAPI.writeErrorLogs(`incrementing ${audioPath.value} failed ${JSON.stringify(getRes)}`);
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        snackbarStore.setContent(`Error while ${context}, check the logs`, SNACKBAR_TIMEOUT, "error");
        restAPI.writeErrorLogs(`${request} : ${err}`);
    }
}

function loadMilkdropPreset() {
    loadPreset();
}
function toggleViewerMode() {
    projectM.toggleFocusMode();
}
function toggleViewer() {
    projectM.toggleMilkdrop();
}

</script>