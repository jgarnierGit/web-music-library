<template>
    <v-card>
        <ArtistToolbar />
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
                                        <playlist-actions :type="PLAYLIST_TYPES.ARTIST" :value="artist.id" />
                                    </template>
                                </v-toolbar>
                            </v-img>
                            <v-card-text>
                                {{ artist.country_name }}
                            </v-card-text>
                            <v-card-actions>

                                <v-tooltip location="top" origin="auto" :text="tooltipMapEditor(artist.id)">
                                    <template v-slot:activator="{ props }">
                                        <v-btn v-bind="props" color="medium-emphasis" :icon="mapEditionIcon(artist.id)"
                                            size="small" @click="switchEdition(artist)"></v-btn>
                                    </template>
                                </v-tooltip>
                                <v-tooltip v-if="editionId === artist.id" location="top" origin="auto"
                                    text="Cancel edition">
                                    <template v-slot:activator="{ props }">
                                        <v-btn v-bind="props" color="error medium-emphasis" :icon="mdiContentSaveOff"
                                            size="small" @click="cancelEdition(artist.id)"></v-btn>
                                    </template>
                                </v-tooltip>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-infinite-scroll>
    </v-card>
</template>

<script setup lang="ts">
import { mdiCloseCircle, mdiContentSaveEdit, mdiContentSaveOff, mdiMapMarker } from '@mdi/js';
import { PLAYLIST_TYPES, SNACKBAR_TIMEOUT } from '~/commons/constants';
import type { Artist, ArtistMapEditorContext, GeomData } from '~/commons/interfaces';
import { getAPI, putAPI, writeErrorLogs } from '~/commons/restAPI';
import ArtistToolbar from './ArtistToolbar.vue';
import { createGeomData } from '~/commons/utils';
const snackbarStore = useSnackbarStore();
const mapStore = useSpatialMapStore();
const { editionId } = storeToRefs(mapStore);
const { pending: dataPending, data: artistsData, error: dataError } = await useLazyAsyncData('artistsListData', () => loadArtists());

const mapEditionIcon = computed(() => (id: string) => editionId.value === id ? mdiContentSaveEdit : mdiMapMarker);
const tooltipMapEditor = computed(() => (id: string) => editionId.value === id ? "Save edition" : "Edit artist location");



async function switchEdition(artist: Artist) {
    if (editionId.value === artist.id) {
        mapStore.closeEditionId(artist.id);
        try {
            await putAPI(`/api/artist/${artist.id}`, 'saving artist', artist);
            mapStore.updateLayerData(createGeomData([artist]));
        } catch (err) {
            snackbarStore.setContent(`Error while loading saving artist ${artist.name}, check the logs`, SNACKBAR_TIMEOUT, "error");
            writeErrorLogs(`/api/artist/${artist.id} : ${err}`);
        }
    }
    else {
        const editionContext = {} as ArtistMapEditorContext;
        editionContext.artist = artist;
        //TODO can be better typed using geomData
        editionContext.callback = (payload: { countryName: string, geom: any }) => {
            editionContext.artist.country_name = payload.countryName;
            editionContext.artist.geom = payload.geom;
        }
        mapStore.openEditionForId(artist.id, editionContext);
    }
}

function cancelEdition(id: string) {
    mapStore.closeEditionId(id);
}

async function loadArtists() {
    const res = await getAPI(`/api/artist/list`, 'loading artists list');
    if (!res) {
        return;
    }
    mapStore.updateLayerData(createGeomData(res.artists.filter((artist: Artist) => artist.geom)));
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

</script>

<style>
.badge-toolbar {
    pointer-events: none !important;
}
</style>