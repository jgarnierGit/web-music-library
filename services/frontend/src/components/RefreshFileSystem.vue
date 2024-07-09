<template>
    <v-list-item value="scan" :ripple="false" :active="false" v-if="!!refreshJobId">
        <template v-slot:prepend>
            <v-icon>
                <v-progress-circular indeterminate :width="3" :size="25">
                    <template v-slot:default :size="20"> {{ showProgress }} </template>
                </v-progress-circular>
            </v-icon>
        </template>
        <template v-slot:append>
            <v-btn :icon="mdiCloseBox" size="small" color="error" variant="text" @click="cancelJob()" />
        </template>
        <v-list-item-title>Scanning... ({{ refreshingCurrentState }} files)</v-list-item-title>
    </v-list-item>

    <v-list-item value="scan" :ripple="false" :active="false" v-else>
        <template v-slot:prepend>
            <v-icon>{{ mdiRadar }}</v-icon>
        </template>
        <v-list-item-title>Scan your music</v-list-item-title>
        <v-tooltip activator="parent" location="end">Refresh from filesystem</v-tooltip>
        <v-overlay activator="parent" location-strategy="connected" scroll-strategy="close" v-model="overlay">
            <v-card class="pa-0 ma-0">
                <v-list>
                    <v-list-item @click="refresh(false)" density="compact" variant="plain">
                        <template v-slot:prepend>
                            <v-icon size="small">{{ mdiTimerRefresh }}</v-icon>
                        </template>Fast
                        <v-tooltip activator="parent" location="end">Add new musics only</v-tooltip>
                    </v-list-item>
                    <v-list-item @click="refresh(true)" density="compact" variant="plain">
                        <template v-slot:prepend>
                            <v-icon size="small">{{ mdiFolderRefresh }}</v-icon>
                        </template>Deep
                        <v-tooltip activator="parent" location="end">Update everything</v-tooltip>
                    </v-list-item>
                </v-list>
            </v-card>
        </v-overlay>
    </v-list-item>
</template>

<script setup lang="ts">
import { mdiCloseBox, mdiFolderRefresh, mdiRadar, mdiTimerRefresh } from '@mdi/js';
import { SNACKBAR_TIMEOUT } from '~/commons/constants';
import { deleteAPI, getAPI, writeErrorLogs } from '~/commons/restAPI';
const snackbarStore = useSnackbarStore();
const fileSystemStore = useFilesystemStore();
const { refreshJobId, refreshingCurrentState } = storeToRefs(fileSystemStore);
const overlay = ref(false);
const refreshJobContent = ref();

// retracted = true
const props = defineProps<{ rail: boolean }>();

const showProgress = computed(() => props.rail ? (refreshingCurrentState.value > 999 ? '+999' : refreshingCurrentState.value) : "");
watch(refreshJobId, async (newVal) => {
    if (newVal) {
        refreshJobContent.value = await getAPI(`/api/job/${newVal}`, "get refresh filesystem job status");
    } else {
        refreshJobContent.value = undefined;
    }
});

watch(refreshJobContent, async (jobRes) => {
    if (jobRes) {
        if (!jobRes) {
            writeErrorLogs(`Job ${refreshJobId.value} can't be reached`);
            fileSystemStore.clearRefreshJobId();
            return;
        }
        if (jobRes.task_status === "FAILURE") {
            snackbarStore.setContent("Refresh filesystem failed. Check server logs for more details", SNACKBAR_TIMEOUT, "error");
            fileSystemStore.clearRefreshJobId();
            return;
        }
        else if (jobRes.task_status === "SUCCESS") {
            snackbarStore.setContent("Refresh filesystem done", SNACKBAR_TIMEOUT, "success");
            fileSystemStore.clearRefreshJobId();
            return;
        }
        else if (["PROGRESS", "PENDING"].includes(jobRes.task_status)) {
            console.log("progress pending")
            fileSystemStore.updateCurrentState(jobRes.task_result ? jobRes.task_result.current : 0);
            setTimeout(async () => {
                if (!refreshJobId.value) {
                    return
                }
                refreshJobContent.value = await getAPI(`/api/job/${refreshJobId.value}`, "get refresh filesystem job status")
            }, 2000);
        }
        else {
            console.log(jobRes.task_status);
        }
    }
})


async function refresh(forceRefresh: boolean) {
    overlay.value = false;
    const jobRes = await getAPI(`/api/folder/refresh?force=${forceRefresh}`, `Scanning filesystem ${forceRefresh ? 'deeply' : 'quickly'}`)
    if (!jobRes) {
        return;
    }
    fileSystemStore.setRefreshJobId(jobRes.result);
}

async function cancelJob() {
    snackbarStore.setContent("Cancelling filesystem cache...", SNACKBAR_TIMEOUT, "warning");
    await deleteAPI(`/api/job/${refreshJobId.value}`, "cancel refresh filesystem job");
    fileSystemStore.clearRefreshJobId();
    snackbarStore.setContent("Cancelled filesystem cache.", SNACKBAR_TIMEOUT, "success");
}

</script>

<style>
.v-progress-circular__content {
    font-size: small;
    position: relative;
    top: 25px;
}
</style>