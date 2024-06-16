<template>
    <v-container fluid>
        <v-row dense>
            <v-col v-for="artist in artistsList.artists" :key="artist.id">
                <v-card>
                    <v-skeleton-loader type="image" boilerplate class="align-end">
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
                        <v-tooltip v-if="editionId === artist.id" location="top" origin="auto" text="Cancel edition">
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
</template>

<script setup lang="ts">
import { mdiContentSaveEdit, mdiContentSaveOff, mdiMapMarker } from '@mdi/js';
import axios from 'axios';
import { API_BASE_URL } from '~/commons/constants';
import type { Artist, ArtistList, ArtistMapEditorContext } from '~/commons/interfaces';

const mapStore = useSpatialMapStore();
const { editionId } = storeToRefs(mapStore);
const artistsList = defineModel({ type: {} as PropType<ArtistList>, required: true });

const mapEditionIcon = computed(() => (id: string) => editionId.value === id ? mdiContentSaveEdit : mdiMapMarker);
const tooltipMapEditor = computed(() => (id: string) => editionId.value === id ? "Save edition" : "Edit artist location")

async function switchEdition(artist: Artist) {
    if (editionId.value === artist.id) {
        mapStore.closeEditionId(artist.id);
        await axios.put(`${API_BASE_URL}/api/artist/${artist.id}`, artist);
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
const mock_data = {} as ArtistList;
mock_data




</script>