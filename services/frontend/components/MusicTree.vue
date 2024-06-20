<template>
    <v-card>
        <v-toolbar title="File System" density="compact" />
        <v-container class="pa-0">
            <v-skeleton-loader type="list-item" v-if="folderPending" />
            <v-alert density="compact" :icon="mdiCloseCircle" v-else-if="folder.error" color="error" variant="outlined">
                [{{ fileSystemRoot }}] Parsing content error ...
                <v-divider color="error"></v-divider>
                Server log: "{{ folder.error }}"
            </v-alert>
            <v-list v-else height="40vh">
                <MusicTreeGroup v-model:node="folder" />
            </v-list>
        </v-container>
    </v-card>
</template>
<script setup lang="ts">
import axiosInstance from '~/axiosInstance';
import MusicTreeGroup from './MusicTreeGroup.vue';
import { mdiCloseCircle } from '@mdi/js';
const fileSystemRoot = ref("/music")

const { pending: folderPending, data: folder } = await useLazyAsyncData(`folderContent-ROOT`, () => loadFolderContent());

async function loadFolderContent() {
    try {
        // load root content
        const getRes = await axiosInstance.post('/api/folder/list');
        if (getRes.status !== 200) {
            console.error(getRes.data); // TODO extract to snackBar.
            return;
        }
        return getRes.data;
    } catch (err) {
        console.error(`error with the server, make sure it is started ${err}, or check its logs`)
    }

}
</script>