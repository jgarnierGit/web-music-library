<template>
    <v-infinite-scroll :height="300" :items="artistsData.artists" :onLoad="load">
        <v-container fluid>
            <v-row dense justify="start">
                <template cols="3" v-for="artist in artistsData.artists" :key="artist.id">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-card width="10vw" height="10vw" min-width="200px" min-height="200px"
                            :class="[{ 'on-hover': isHovering }, 'd-flex', 'flex-column', 'text-white', 'ma-1']"
                            :elevation="isHovering ? 12 : 2" v-bind="props">
                            <v-img src="/default_artist.png" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>
                                <v-card-title class="text-h6 artist-card-title">
                                    {{ artist.name }}
                                </v-card-title>
                                <v-card-text class="artist-card-bottom ma-0 pa-0">
                                    <p class=" text-body-1 font-weight-bold">
                                        <button @click="genresView()">Genre +</button>
                                        <!-- TODO add hover list genre on click -->
                                    </p>
                                    <p class="text-caption font-weight-medium">
                                        <button @click="albumsView()">{{ artist.albums_count }} albums</button> -
                                        <button @click="tracksView()">{{ artist.tracks_count }}
                                            tracks</button>
                                    </p>
                                    <v-card-actions
                                        :class="[{ 'hide-playlist-actions': !isHovering }, 'justify-center']">
                                        <PlaylistActions :type="PLAYLIST_TYPES.ARTIST" :value="[artist.id]"
                                            variant="text" density="default" />
                                    </v-card-actions>
                                </v-card-text>
                            </v-img>
                        </v-card>
                    </v-hover>
                </template>
            </v-row>
        </v-container>
    </v-infinite-scroll>
</template>
<script setup lang="ts">
import { PLAYLIST_TYPES } from '~/commons/constants';
import PlaylistActions from '../PlaylistActions.vue';

const dbCacheStore = useDbCacheStore();
const { artistsData } = storeToRefs(dbCacheStore);

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
.artist-card-title {
    text-wrap: stable;
    opacity: 1 !important;
    text-align: center;
}

.artist-card-bottom {
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;

    button:hover {
        text-decoration: underline;
    }
}

.hide-playlist-actions {
    visibility: hidden;
}
</style>