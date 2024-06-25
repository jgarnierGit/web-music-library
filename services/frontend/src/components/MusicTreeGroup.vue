<template>
    <v-list-group :subgroup="true" :key="musicFolder.path">
        <template v-slot:activator="{ props, isOpen }">
            <v-list-item v-if="hasContent" v-bind="props" :title="musicFolder.name"
                :prepend-icon="folderIcon(musicFolder, isOpen)" />
            <v-list-item v-else v-bind="props" :title="musicFolder.name" :prepend-icon="mdiFolder"
                @click="loadFolderContent(musicFolder)" />
        </template>
        <v-skeleton-loader type="list-item" v-if="loading"></v-skeleton-loader>
        <v-list-item v-for="(file, i) in musicFolder.musics" @click="startPlay(file.music)" :ripple="!file.error"
            :prepend-icon="musicIcon(file)" :base-color="hasErrorStyle(file)"
            v-on:mouseover="hoveringId = file.music.id" v-on:mouseleave="hoveringId = undefined">
            <v-list-item-title v-if="!file.error">{{ file.music.name }} </v-list-item-title>
            <v-alert density="compact" :icon="mdiCloseCircle" v-else color="error" variant="outlined">
                <b>{{ file.music.name }}</b> - Parsing file error ...
                <v-divider color="error"></v-divider>
                Server log: "{{ file.error }}"
            </v-alert>
        </v-list-item>

        <MusicTreeGroup v-for="(subFolder, i) in musicFolder.folders" v-model:node="musicFolder.folders[i]"
            :depth="depth + 1" />
    </v-list-group>
    <!--  -->

</template>

<script setup lang="ts">
import { mdiCloseCircle, mdiFileMusicOutline, mdiFolder, mdiFolderOpen, mdiPlay } from '@mdi/js';
import axiosInstance from '~/axiosInstance';
import { SNACKBAR_TIMEOUT } from '~/commons/constants';
import type { File, Folder, Music } from '~/commons/interfaces';
import { postTauriAPI, writeErrorLogs } from '~/commons/tauri';
import { usePlaylistStore } from '~/stores/playlist';
import { useSnackbarStore } from '~/stores/snackbar';
const playlist = usePlaylistStore();
const snackbarStore = useSnackbarStore();

const hoveringId = ref<string>();
const loading = ref(false);

const folderIcon = computed(() => (folder: Folder, isOpen: boolean) => isOpen ? mdiFolderOpen : mdiFolder) // TODO folder.path === hoveringId.value ? mdiPlay :
const musicIcon = computed(() => (file: File) => file.error ? '' : file.music.id === hoveringId.value ? mdiPlay : mdiFileMusicOutline)
const hasErrorStyle = computed(() => (file: File) => file.error ? 'error' : '')

const props = withDefaults(defineProps<{ depth?: number }>(), {
    depth: 0
});
const musicFolder = defineModel('node', { type: {} as PropType<Folder>, required: true });
const hasContent = computed(() => !!musicFolder.value.musics.length || !!musicFolder.value.folders.length);

function startPlay(music: Music) {
    playlist.setCurrentPlaying(music);
}

async function loadFolderContent(subFolder: Folder) {
    loading.value = true;
    try {
        // load root content
        const getRes = await postAPI('/api/folder/list', 'loading sub folder content', { path: subFolder.path });
        if (!getRes) {
            return;
        }
        musicFolder.value.folders = getRes.data.folders;
        musicFolder.value.musics = getRes.data.musics;
    } finally {
        loading.value = false;
    }
}

async function postAPI(request: string, context: string, playload: any) {
    try {
        const getRes = await postTauriAPI(request, context, playload);
        if (getRes.status !== 200) {
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        snackbarStore.setContent(`Error while ${context}, check the logs`, SNACKBAR_TIMEOUT, "error");
        writeErrorLogs(`${request} : ${err}`);
    }
}
</script>