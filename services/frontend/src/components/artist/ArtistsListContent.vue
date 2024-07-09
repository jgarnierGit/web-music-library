<template>
    <v-infinite-scroll :height="300" :items="artistsData.artists" item-height="48" @load="load">
        <v-list-item :title="`${artist.name}`" v-for="(artist, index) in artistsData.artists" :key="artist.id"
            v-on:mouseover="hoveringArtistId = artist.id" v-on:mouseleave="hoveringArtistId = undefined">
            <v-list-item-subtitle class="artist-list-item">
                <button @click="albumsView()">{{ artist.albums_count }} albums</button> - <button
                    @click="tracksView()">{{ artist.tracks_count }}
                    tracks</button>
                <v-divider></v-divider>
                <v-chip @click="genresView()" color="secondary" size="small" variant="outlined" density="compact">
                    Genre1
                </v-chip> <v-chip @click="genresView()" color="secondary" size="small" variant="outlined"
                    density="compact">
                    Genre2
                </v-chip>
            </v-list-item-subtitle>
            <template v-slot:prepend>
                <v-icon v-if="hoveringArtistId != artist.id">{{ mdiAccount }}</v-icon>
                <PlaylistActions v-else :type="PLAYLIST_TYPES.ARTIST" :value="[artist.id]" />
            </template>
        </v-list-item>
    </v-infinite-scroll>
</template>

<script setup lang="ts">
import { mdiAccount } from '@mdi/js';
import { PLAYLIST_TYPES } from '~/commons/constants';
const dbCacheStore = useDbCacheStore();
const { artistsData } = storeToRefs(dbCacheStore);
const hoveringArtistId = ref();

defineProps<{ load: any }>()

function albumsView() {
    console.log("album");
}

function tracksView() {
    console.log("songs");
}

function genresView() {
    console.log("genre");
}
</script>
<style>
.artist-list-item {
    button:hover {
        text-decoration: underline;
    }
}
</style>