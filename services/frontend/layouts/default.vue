<template>
    <v-app class="app">
        <v-main>
            <v-container>
                <slot />
            </v-container>
        </v-main>
        <v-footer app color="grey" height="44" center class="opacity-90">
            <v-row justify="center">
                <v-col cols="4"></v-col>
                <v-col cols="4">
                    <MusicPlayer />
                </v-col>
                <v-col cols="4"></v-col>
            </v-row>
        </v-footer>
        <Milkdrop v-if="isVisible" />

    </v-app>
</template>

<script setup lang="ts">
import MusicPlayer from '~/components/MusicPlayer.vue';
const projectM = useProjectMStore();
const { isVisible } = storeToRefs(projectM);

</script>

<style>
.v-application {
    background: none !important;
}
</style>