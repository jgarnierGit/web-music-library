<template>
    <v-toolbar density="compact">
        <v-toolbar-title>{{ title }}
            <v-badge :content="`${countLoaded} / ${isRefreshing ? '...' : dbCount}`" inline />
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
            <slot />
            <v-divider vertical></v-divider>
            <v-btn icon @click="refreshCount()" :disabled="isRefreshing"><v-icon>{{ mdiRefresh }}</v-icon></v-btn>
        </v-toolbar-items>
    </v-toolbar>
</template>

<script setup lang="ts">
import { mdiRefresh } from '@mdi/js';
import { writeInfoLogs } from '~/commons/restAPI';
const fileSystemStore = useFilesystemStore();
const { refreshJobId, refreshingCurrentState } = storeToRefs(fileSystemStore);
const previousRefreshingState = ref();

const props = withDefaults(defineProps<{
    title: string,
    countLoaded: number,
    countRefreshCallback: () => Promise<any>,
    autoRefresh?: boolean
}>(), {
    autoRefresh: false
});
const { pending: countPending, data: dbCount } = await useLazyAsyncData(`${props.title}CountTotal`, () => props.countRefreshCallback());
const isRefreshing = computed(() => countPending.value);

watch(refreshJobId, (newVal) => {
    if (!props.autoRefresh) {
        return;
    }
    if (newVal) {
        batchRefreshCount();
    }
});

function batchRefreshCount() {
    if (!refreshJobId.value) {
        writeInfoLogs("Stopped auto refresh")
        return
    }
    if (refreshingCurrentState.value !== previousRefreshingState.value) {
        writeInfoLogs("auto refresh...")
        previousRefreshingState.value = refreshingCurrentState.value;
        refreshCount();
    }
    else {
        writeInfoLogs("skipping auto refresh")
    }


    setTimeout(() => {
        batchRefreshCount()
    }, 5000);
}

async function refreshCount() {
    countPending.value = true
    dbCount.value = await props.countRefreshCallback();
    countPending.value = false;
}
</script>