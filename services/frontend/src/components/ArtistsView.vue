<template>
    <v-card>
        <NavigatorToolbar title="Artists" :countLoaded="countLoadedArtists" :countRefreshCallback="refreshCountArtists"
            :autoRefresh="true">
            <v-btn v-if="!isCard" @click="isCard = !isCard"><v-icon>{{ mdiAccountBoxOutline }}</v-icon>
                <v-tooltip activator="parent" location="top">Display as cards</v-tooltip>
            </v-btn>
            <v-btn v-else @click="isCard = !isCard"><v-icon>{{ mdiFormatListText }}</v-icon>
                <v-tooltip activator="parent" location="top">Display in list</v-tooltip></v-btn>
        </NavigatorToolbar>
        <v-container fluid v-if="dataPending">
            <v-row dense justify="start">
                <v-col cols="3" v-for="n in 3">
                    <v-skeleton-loader type="card"></v-skeleton-loader>
                </v-col>
            </v-row>
        </v-container>
        <v-container fluid v-else-if="dataError">
            <v-alert density="compact" :icon="mdiCloseCircle" color="error" variant="outlined">
                Artists access error ...
                <v-divider color="error"></v-divider>
                Server log: "{{ dataError }}"
            </v-alert>
        </v-container>
        <ArtistsListContent v-else-if="!isCard" :load="load"></ArtistsListContent>
        <ArtistsCardContent v-else-if="isCard" :load="load"></ArtistsCardContent>
    </v-card>
</template>

<script setup lang="ts">
import { mdiAccountBoxOutline, mdiCloseCircle, mdiFormatListText } from '@mdi/js';
import type { Artist } from '~/commons/interfaces';
import { getAPI, writeInfoLogs } from '~/commons/restAPI';
import { createGeomData } from '~/commons/utils';
import NavigatorToolbar from '~/components/NavigatorToolbar.vue';
import ArtistsListContent from './artist/ArtistsListContent.vue';
import ArtistsCardContent from './artist/ArtistsCardContent.vue';
const mapStore = useSpatialMapStore();
const dbCacheStore = useDbCacheStore();
const { artistsData, countLoadedArtists } = storeToRefs(dbCacheStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('artistsListData', () => loadArtists());
const isCard = ref(true);


watch(artistsData, (newVal) => {
    if (newVal) {
        mapStore.updateLayerData(createGeomData(artistsData.value.artists.filter((artist: Artist) => artist.geom)));
    }
});

async function loadArtists() {
    if (artistsData.value) {
        writeInfoLogs("skip artist refresh");
        return
    }
    const res = await getAPI(`/api/artist/list`, 'loading artists list');
    if (!res) {
        return;
    }
    mapStore.updateLayerData(createGeomData(res.artists.filter((artist: Artist) => artist.geom)));
    dbCacheStore.setArtistsData(res);
    return res;
}

//@ts-ignore
async function load({ done }) {
    const res: any = await getAPI(`/api/artist/list?offset=${artistsData.value.artists.length}`, 'loading more artists');
    if (res.artists && res.artists.length > 0) {
        artistsData.value.artists.push(...res.artists);
        done('ok')
    }
    else {
        done('empty')
    }
}


async function refreshCountArtists() {
    const res = await getAPI(`/api/artist/count`, 'refresh artists count');
    if (!res) {
        return "No data";
    }
    return res.result;
}

</script>

<style>
.badge-toolbar {
    pointer-events: none !important;
}
</style>