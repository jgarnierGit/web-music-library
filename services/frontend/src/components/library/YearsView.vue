<template>
    <LibraryContentView title="Years" :countLoaded="countLoadedYears" :refreshCountCallback="refreshCount"
        :autoRefresh="true" :dataPending="dataPending" :dataError="dataError">
        WIP
    </LibraryContentView>
</template>

<script setup lang="ts">
import type { ContentList, Year } from '~/commons/interfaces';
import { getAPI, writeInfoLogs } from '~/commons/restAPI';

const dbCacheStore = useDbCacheStore();
const { yearsData, countLoadedYears } = storeToRefs(dbCacheStore);
const fileSystemStore = useFilesystemStore();
const { isCard } = storeToRefs(fileSystemStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('yearsListData', () => loadContents());

async function refreshCount() {
    const res = await getAPI(`/api/years/count`, 'refresh years count');
    if (!res) {
        return "No data";
    }
    return res.result;
}

async function loadContents() {
    if (yearsData.value) {
        writeInfoLogs("skip albums refresh");
        return
    }

    return await reloadContents();
}


async function reloadContents() {
    dataPending.value = true;
    return Promise.resolve();
    const res = await getAPI(`/api/years/list`, 'loading years list');

    if (!res) {
        return;
    }
    dbCacheStore.setYearsData({ contents: res.contents } as ContentList<Year>);
    dataPending.value = false;
    return res
}

</script>