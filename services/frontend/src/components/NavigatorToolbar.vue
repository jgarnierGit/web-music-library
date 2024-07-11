<template>
    <v-toolbar density="compact">
        <v-toolbar-title>{{ title }}
            <v-badge :content="`${countLoaded.toLocaleString()} / ${isRefreshing ? '...' : dbCount.toLocaleString()}`"
                inline />
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
            <slot />
        </v-toolbar-items>
    </v-toolbar>
</template>

<script setup lang="ts">
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

watch(refreshJobId, (newVal, oldVal) => {
    if (!props.autoRefresh) {
        return;
    }
    if (newVal) {
        batchRefreshCount();
    }
    else if (oldVal) {
        // refresh one last time
        refreshCount();
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
    }, 10000);
}

async function refreshCount() {
    countPending.value = true
    dbCount.value = await props.countRefreshCallback();
    countPending.value = false;
}
</script>