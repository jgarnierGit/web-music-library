<template>
    <v-card>
        <v-toolbar density="compact">
            <v-toolbar-title>Artists
                <v-badge v-if="!countPending" :content="artistsCount.result" inline />
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
                <v-btn icon v-if="countPending" variant="text" readonly>
                    <v-progress-circular :size="20" :width="2" indeterminate></v-progress-circular>
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>
        <v-container fluid v-if="dataPending">
            <v-row dense justify="start">
                <v-col cols="3" v-for="n in 3">
                    <v-skeleton-loader type="card"></v-skeleton-loader>
                </v-col>
            </v-row>
        </v-container>
        <v-infinite-scroll v-else :height="300" :items="artistsData.artists" :onLoad="load">
            <v-container fluid>
                <v-row dense justify="start">
                    <v-col cols="3" v-for="artist in artistsData.artists" :key="artist.id">
                        <v-card>
                            <v-img src="/default_artist.png" class="align-end"
                                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>
                                <v-card-title class="text-white" v-text="artist.name"></v-card-title>
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
import { mdiContentSaveEdit, mdiContentSaveOff, mdiMapMarker } from '@mdi/js';
import axiosInstance from '~/axiosInstance';
import type { Artist, ArtistMapEditorContext } from '~/commons/interfaces';

const mapStore = useSpatialMapStore();
const { editionId } = storeToRefs(mapStore);
const { pending: countPending, data: artistsCount } = await useLazyAsyncData('artistsListCount', () => getAPI(`/api/artist/count`));
const { pending: dataPending, data: artistsData } = await useLazyAsyncData('artistsListData', () => loadArtists());

const mapEditionIcon = computed(() => (id: string) => editionId.value === id ? mdiContentSaveEdit : mdiMapMarker);
const tooltipMapEditor = computed(() => (id: string) => editionId.value === id ? "Save edition" : "Edit artist location")

async function switchEdition(artist: Artist) {
    if (editionId.value === artist.id) {
        mapStore.closeEditionId(artist.id);
        await axiosInstance.put(`/api/artist/${artist.id}`, artist);
        // TODO reintroduce the snacbar
    }
    else {
        const editionContext = {} as ArtistMapEditorContext;
        editionContext.artist = artist;
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
    const res = await getAPI(`/api/artist/list`);
    mapStore.addLayer(res.artists.filter((artist: Artist) => artist.geom));
    return res;
}

async function getAPI(request: string) {
    try {
        const getRes = await axiosInstance.get(request);
        if (getRes.status !== 200) {
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        console.error(`error with the server, make sure it is started ${err}`)
    }
}

async function api() {
    return await getAPI(`/api/artist/list?offset=${artistsData.value.artists.length}`);
}
//@ts-ignore
async function load({ done }) {
    // Perform API call
    const res: any = await api()
    if (res.artists && res.artists.length > 0) {
        artistsData.value.artists.push(...res.artists)
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