<template>
    <v-row justify="center">
        <v-col>
            <audio ref="audioPlayer" controls preload="auto" autoplay="true" crossOrigin="anonymous" loop
                controlsList="nodownload" :src="audioPath" style="height:100%">
                Your browser does not support the audio element.
            </audio>

        </v-col>
        <v-col style="vertical-align: middle">
            <v-tooltip location="top" origin="auto" :text="nextSongTooltip">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" :icon="mdiSkipNext" variant="text" @click="playNext()" />
                </template>
            </v-tooltip>
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
import { AUDIO_BASE_URL } from '~/commons/constants';
import { usePlaylistStore } from '~/stores/playlist';
import { mdiSwapHorizontal, mdiMonitorOff, mdiMonitor, mdiFullscreen, mdiFullscreenExit, mdiSkipNext } from '@mdi/js';
import { postAPI, writeErrorLogs, writeInfoLogs } from '~/commons/restAPI';
const projectM = useProjectMStore();

const audioPath = ref<string>();
const playlist = usePlaylistStore();
const audioPlayer = ref();
const { currentPlaying, nextSong } = storeToRefs(playlist);
const { isVisible, isFocused } = storeToRefs(projectM);

// audioPath.value = `/demo.mp3`; //TODO  mock file system

const viewerIcon = computed(() => isVisible.value ? mdiMonitorOff : mdiMonitor)
const viewerIconMode = computed(() => isFocused.value ? mdiFullscreenExit : mdiFullscreen)
const focusTooltip = computed(() => isFocused.value ? "Background mode" : "Focus mode")
const nextSongTooltip = computed(() => nextSong && nextSong.value ? `${nextSong.value.artist?.name} - ${nextSong.value.name}` : 'Play next song');

onMounted(() => {
    audioPlayer.value.onerror = function (err: any) {
        writeErrorLogs(`Audio PLayer failed to read audio ${audioPath.value}, ${JSON.stringify(err)}`);
    }
    audioPlayer.value.onended = function () {
        playlist.playNextSong();
    }
})

watch(currentPlaying, async (newVal) => {
    if (newVal) {
        audioPath.value = `${AUDIO_BASE_URL}${newVal.path}`;

        writeInfoLogs(`playing ${audioPath.value}`);
        enableAudio(audioPlayer.value, false);
        const response = await postAPI(`/api/music/${newVal.id}/increment/`, 'incrementing play count for artist');
        if (!response) {
            return
        }
        playlist.setRandomNextSong();
    }
})

function playNext() {
    playlist.playNextSong();
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