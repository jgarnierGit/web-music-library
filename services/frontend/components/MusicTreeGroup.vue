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
import type { File, Folder, Music } from '~/commons/interfaces';
import { usePlaylistStore } from '~/stores/playlist';
const playlist = usePlaylistStore();

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
        const getRes = await axiosInstance.post('/api/folder/list', { path: subFolder.path });
        if (getRes.status !== 200) {
            console.error(getRes.data); // TODO extract to snackBar.
            return;
        }
        musicFolder.value.folders = getRes.data.folders;
        musicFolder.value.musics = getRes.data.musics;
    } catch (err) {
        console.error(`error with the server, make sure it is started ${err}, or check its logs`)
    } finally {
        loading.value = false;
    }
}
</script>