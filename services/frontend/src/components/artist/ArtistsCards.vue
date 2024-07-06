<template>
    <v-card>
        <NavigatorToolbar title="Artists" :countLoaded="countLoadedArtists" :countRefreshCallback="refreshCountArtists"
            :autoRefresh="true" />
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
        <v-infinite-scroll v-else :height="300" :items="artistsData.artists" :onLoad="load">
            <v-container fluid>
                <v-row dense justify="start">
                    <v-col cols="3" v-for="artist in artistsData.artists" :key="artist.id">
                        <v-card max-width="20vw">
                            <v-img src="/default_artist.png" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>

                                <v-toolbar color="transparent">
                                    <v-toolbar-title class="text-white" v-text="artist.name"></v-toolbar-title>
                                    <template v-slot:append>
                                        <PlaylistActions :type="PLAYLIST_TYPES.ARTIST" :value="artist.id" />
                                    </template>
                                </v-toolbar>
                            </v-img>
                            <v-card-text>
                                {{ artist.country_name }}
                            </v-card-text>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-infinite-scroll>
    </v-card>
</template>

<script setup lang="ts">
import { mdiCloseCircle } from '@mdi/js';
import { PLAYLIST_TYPES } from '~/commons/constants';
import type { Artist } from '~/commons/interfaces';
import { getAPI, writeInfoLogs } from '~/commons/restAPI';
import { createGeomData } from '~/commons/utils';
import PlaylistActions from '~/components/PlaylistActions.vue';
import NavigatorToolbar from '~/components/NavigatorToolbar.vue';
const mapStore = useSpatialMapStore();
const dbCacheStore = useDbCacheStore();
const { artistsData } = storeToRefs(dbCacheStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('artistsListData', () => loadArtists());
const countLoadedArtists = computed(() => artistsData.value ? artistsData.value.artists.length : 0)

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
        artistsData.value.artists.push(...res.artists)
        mapStore.updateLayerData(createGeomData(res.artists.filter((artist: Artist) => artist.geom)));
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