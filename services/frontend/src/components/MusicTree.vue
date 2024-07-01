<template>
    <v-card>
        <v-toolbar title="File System" density="compact" />
        <v-container class="pa-0">
            <v-skeleton-loader type="list-item" v-if="folderPending" />
            <v-alert density="compact" :icon="mdiCloseCircle" v-else-if="folderError" color="error" variant="outlined">
                Fetching content error ...
                <v-divider color="error"></v-divider>
                Server log: "{{ folderError }}"
            </v-alert>
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
import MusicTreeGroup from './MusicTreeGroup.vue';
import { mdiCloseCircle } from '@mdi/js';
import { SNACKBAR_TIMEOUT } from '~/commons/constants';
import { postAPI, writeInfoLogs, writeWarnLogs } from '~/commons/restAPI';

const snackbarStore = useSnackbarStore();
const fileSystemRoot = ref("/music")
const { pending: folderPending, data: folder, error: folderError } = await useLazyAsyncData(`folderContent-ROOT`, () => loadFolderContent());

async function loadFolderContent() {
    snackbarStore.setContent(`Loading music content`, SNACKBAR_TIMEOUT, "info");
    // load root content
    const getRes = await postAPI('/api/folder/list', 'loading file system root tree');
    if (!getRes) {
        writeWarnLogs("Got empty system tree");
        return
    }
    writeInfoLogs(`Loaded system tree`);
    return getRes;
}
</script>