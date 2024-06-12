<template>
    <v-app>
        <v-main>
            <v-container>
                <slot />
            </v-container>

        </v-main>
        <v-footer app color="grey" height="44" center>
            <v-row justify="center">
                <MusicPlayer />
            </v-row>
        </v-footer>
    </v-app>
</template>

<script setup lang="ts">
import MusicPlayer from '~/components/MusicPlayer.vue';

</script>