<template>
    <v-list-group :subgroup="true" :key="musicFolder.path">
        <template v-slot:activator="{ props, isOpen }">
            <v-list-item v-if="hasContent" v-bind="props" :title="musicFolder.name"
                v-on:mouseover="hoveringFolder = true" v-on:mouseleave="hoveringFolder = false">
                <template v-slot:prepend>
                    <v-icon v-if="!hoveringFolder">{{ folderIcon(isOpen) }}</v-icon>
                    <PlaylistActions v-else :type="PLAYLIST_TYPES.FOLDER" :value="[musicFolder.path]" />
                </template>

            </v-list-item>

            <v-list-item v-else v-bind="props" :title="musicFolder.name" @click="loadFolderContent(musicFolder)"
                v-on:mouseover="hoveringFolder = true" v-on:mouseleave="hoveringFolder = false">
                <template v-slot:prepend>
                    <v-icon v-if="!hoveringFolder">{{ mdiFolder }}</v-icon>
                    <PlaylistActions v-else :type="PLAYLIST_TYPES.FOLDER" :value="[musicFolder.path]" />
                </template>

            </v-list-item>
        </template>
        <v-skeleton-loader type="list-item" v-if="loading"></v-skeleton-loader>
        <v-list-item v-for="(file, i) in musicFolder.musics" @click="startPlay(file)" :ripple="!file.error"
            :prepend-icon="musicIcon(file)" :base-color="hasErrorStyle(file)"
            v-on:mouseover="hoveringId = file.music.id" v-on:mouseleave="hoveringId = undefined">
            <v-list-item-title v-if="!file.error">{{ file.music.name }} </v-list-item-title>
            <v-alert density="compact" :icon="mdiCloseCircle" v-else color="error" variant="outlined">
                <b>{{ file.music.name }}</b> - Parsing file error ...
                <v-divider color="error"></v-divider>
                Server log: "{{ file.error }}"
            </v-alert>
            <template v-slot:append><v-icon color="warning" v-if="!file.saved">{{
                mdiContentSaveAlertOutline
                    }}

                </v-icon>
            </template>
            <v-tooltip v-if="!file.saved" activator="parent" location="end">Music not saved, will not be available
                in
                filtering</v-tooltip>
        </v-list-item>

        <MusicTreeGroup v-for="(subFolder, i) in musicFolder.folders" v-model:node="musicFolder.folders[i]"
            :depth="depth + 1" />
    </v-list-group>
</template>

<script setup lang="ts">
import { mdiCloseCircle, mdiContentSaveAlertOutline, mdiFileMusicOutline, mdiFolder, mdiFolderOpen, mdiPlay } from '@mdi/js';
import { PLAYLIST_TYPES } from '~/commons/constants';
import type { File, Folder, Music } from '~/commons/interfaces';
import { postAPI } from '~/commons/restAPI';
import PlaylistActions from '~/components/PlaylistActions.vue';
import { usePlaylistStore } from '~/stores/playlist';
const playlist = usePlaylistStore();
const dbCacheStore = useDbCacheStore();

const hoveringId = ref<string>();
const hoveringFolder = ref(false);
const loading = ref(false);

const folderIcon = computed(() => (isOpen: boolean) => isOpen ? mdiFolderOpen : mdiFolder)
const musicIcon = computed(() => (file: File) => file.error ? '' : file.music.id === hoveringId.value ? mdiPlay : mdiFileMusicOutline)
const hasErrorStyle = computed(() => (file: File) => file.error ? 'error' : '')

const props = withDefaults(defineProps<{ depth?: number }>(), {
    depth: 0
});
const musicFolder = defineModel('node', { type: {} as PropType<Folder>, required: true });
const hasContent = computed(() => !!musicFolder.value.musics.length || !!musicFolder.value.folders.length);

function startPlay(file: File) {
    playlist.setCurrentPlaying(file);
}

async function loadFolderContent(subFolder: Folder) {
    loading.value = true;
    try {
        // load root content
        const getRes = await postAPI('/api/folders/list', 'loading sub folder content', { path: subFolder.path });
        if (!getRes) {
            return;
        }
        musicFolder.value.folders = getRes.folders;
        musicFolder.value.musics = getRes.musics;
        dbCacheStore.updateCountFiles();
    } finally {
        loading.value = false;
    }
}

</script>