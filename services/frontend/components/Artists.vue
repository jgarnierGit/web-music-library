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
        <v-container fluid>
            <v-row dense>
                <v-col v-for="artist in artistsList.artists" :key="artist.id">
                    <v-card max-width="150">
                        <v-skeleton-loader type="image" boilerplate>
                            <v-card-title class="text-gray" v-text="artist.name"></v-card-title>
                        </v-skeleton-loader>
                        <v-card-text>
                            {{ artist.country_name }}
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
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
    </v-card>
</template>

<script setup lang="ts">
import { mdiContentSaveEdit, mdiContentSaveOff, mdiMapMarker } from '@mdi/js';
import axiosInstance from '~/axiosInstance';
import { API_BASE_URL } from '~/commons/constants';
import type { Artist, ArtistList, ArtistMapEditorContext } from '~/commons/interfaces';

const mapStore = useSpatialMapStore();
const { editionId } = storeToRefs(mapStore);
const artistsList = defineModel({ type: {} as PropType<ArtistList>, required: true });
const { pending: countPending, data: artistsCount } = await useLazyAsyncData('artistsList', () => countArtists());

watch(artistsCount, (newCount) => {

})

/** 
const observer = new IntersectionObserver();

const coolElement = document.querySelector("#coolElement");
observer.observe(coolElement);*/


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
        editionContext.callback = (country_name: string) => editionContext.artist.country_name = country_name;
        mapStore.openEditionForId(artist.id, editionContext);
    }
}

function cancelEdition(id: string) {
    mapStore.closeEditionId(id);
}

async function countArtists() {
    try {
        const getRes = await axiosInstance.get(`/api/artist/count`);
        if (getRes.status !== 200) {
            console.error(getRes.data);
            return;
        }
        return getRes.data;
    } catch (err) {
        console.error(`error with the server, make sure it is started ${err}`)
    }

}


</script>

<style>
.badge-toolbar {
    pointer-events: none !important;
}
</style>