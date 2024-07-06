<template>
    <v-app class="app">
        <MusicMenu />
        <v-main v-show="!isFocused">
            <v-container class="background-over-milkdrop">
                <v-row>
                    <v-col>
                        <slot></slot>
                    </v-col>
                    <v-col cols="7" class="opacity-100">
                        <InteractiveMap />
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
        <v-footer app height="50" center class="background-over-milkdrop">
            <v-row justify="center" no-gutters align="center">
                <v-col>
                    <v-row>
                        <v-col v-if="currentPlaying">
                            current playing : {{ currentPlaying.name }} - {{ currentPlaying.artist.name }}
                        </v-col>
                        <v-divider vertical v-if="currentPlaying && filter" />
                        <v-col v-if="filter">
                            current filter : {{ filter.type }} - {{ filter.targetIds }}
                        </v-col>
                    </v-row>
                </v-col>
                <v-col>
                    <MusicPlayer />
                </v-col>
                <v-spacer></v-spacer>
            </v-row>
        </v-footer>
        <Milkdrop v-if="isVisible" />
        <SnackBar></SnackBar>
    </v-app>
</template>

<script setup lang="ts">
import MusicPlayer from '~/components/MusicPlayer.vue';
import Milkdrop from '~/components/Milkdrop.vue';
import SnackBar from '../components/SnackBar.vue';
import MusicMenu from '~/components/MusicMenu.vue';
const projectM = useProjectMStore();
const playlistStore = usePlaylistStore();
const { currentPlaying, filter } = storeToRefs(playlistStore);
const { isVisible, isFocused } = storeToRefs(projectM);

</script>

<style>
.v-application {
    background: none !important;
}

.background-over-milkdrop {
    background-color: rgba(238, 238, 238, 0.80);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
}
</style>