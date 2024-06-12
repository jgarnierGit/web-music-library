<template>
    <v-list-group v-if="hasContent" :subgroup="true" :value="musicFolder.name" :title="musicFolder.name">
        <template v-slot:activator="{ props }">
            <v-list-item v-bind="props" :title="musicFolder.name" />
        </template>
        <v-list-item v-for="(music, i) in musicFolder.musics" :title="music.name" @click="startPlay(music)" />

        <MusicTreeGroup v-for="(folder, i) in musicFolder.folders" v-model="musicFolder.folders[i]"
            :depth="depth + 1" />
    </v-list-group>
    <v-list-item v-else :title="musicFolder.name" />
</template>

<script setup lang="ts">
import type { Folder, Music } from '~/commons/interfaces';
import { usePlaylistStore } from '~/stores/playlist';
const playlist = usePlaylistStore();

withDefaults(defineProps<{ depth?: number }>(), {
    depth: 0
});
const musicFolder = defineModel({ type: {} as PropType<Folder>, required: true });

const hasContent = computed(() => musicFolder.value.musics.length || musicFolder.value.folders.length);

function startPlay(music: Music) {
    playlist.setCurrentPlaying(music);
}

</script>