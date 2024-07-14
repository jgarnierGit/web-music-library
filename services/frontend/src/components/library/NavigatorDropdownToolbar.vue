<template>
    <v-toolbar density="compact">
        <v-toolbar-title justify="center">
            <v-select :items="LIBRARY_VIEWS" v-model="activeNavigatorView.target" density="compact"
                class="navigator-dropdown"></v-select>
            <v-badge
                :content="`${countLoaded.toLocaleString()} / ${isRefreshing ? '...' : (dbCount || 0).toLocaleString()}`"
                inline />
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items>
            <slot />
        </v-toolbar-items>
    </v-toolbar>
</template>

<script setup lang="ts">
import { LIBRARY_VIEWS } from '~/commons/constants';
import { writeInfoLogs } from '~/commons/restAPI';
const fileSystemStore = useFilesystemStore();
const { refreshJobId, refreshingCurrentState, activeNavigatorView } = storeToRefs(fileSystemStore);
const previousRefreshingState = ref();

const props = withDefaults(defineProps<{
    title: string,
    countLoaded: number,
    countRefreshCallback: () => Promise<any>,
    autoRefresh?: boolean,
    toolbarContextId?: string
}>(), {
    autoRefresh: false,
    toolbarContextId: ''
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
<style>
.navigator-dropdown {
    display: inline-flex;

    .v-input__details {
        display: none;
    }
}
</style>