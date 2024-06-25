<template>
    <v-app class="app ">
        <v-main v-show="!isFocused">
            <v-container class="background-over-milkdrop">
                <slot />
            </v-container>
        </v-main>
        <v-footer app height="50" center class="background-over-milkdrop">
            <v-row justify="center">
                <v-col cols="4"></v-col>
                <v-col cols="4">
                    <MusicPlayer />
                </v-col>
                <v-col cols="4"></v-col>
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
const projectM = useProjectMStore();
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