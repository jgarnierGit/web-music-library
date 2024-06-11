<template>
    <v-app>
        <v-main>
            <v-container>
                <slot />
            </v-container>
            <MusicPlayer />
        </v-main>
    </v-app>
</template>

<script setup lang="ts">
import MusicPlayer from '~/components/MusicPlayer.vue';

</script>