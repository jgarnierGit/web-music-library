<template>
    <v-list-group v-if="hasContent" :subgroup="true" :value="musicFolder.name" :title="musicFolder.name">
        <template v-slot:activator="{ props, isOpen }">
            <v-list-item v-bind="props" :title="musicFolder.name" :prepend-icon="folderIcon(isOpen)" />
        </template>
        <v-list-item v-for="(music, i) in musicFolder.musics" :title="music.name" @click="startPlay(music)"
            :prepend-icon="musicIcon(music)" v-on:mouseover="musicHoveringId = music.id"
            v-on:mouseleave="musicHoveringId = undefined" />

        <MusicTreeGroup v-for="(folder, i) in musicFolder.folders" v-model="musicFolder.folders[i]"
            :depth="depth + 1" />
    </v-list-group>
    <v-list-item v-else :title="musicFolder.name" :prepend-icon="mdiFolder" />
</template>

<script setup lang="ts">
import { mdiFileMusicOutline, mdiFolder, mdiFolderOpen, mdiPlay } from '@mdi/js';
import type { Folder, Music } from '~/commons/interfaces';
import { usePlaylistStore } from '~/stores/playlist';
const playlist = usePlaylistStore();

const musicHoveringId = ref<string>();

const folderIcon = computed(() => (isOpen: boolean) => isOpen ? mdiFolderOpen : mdiFolder)

const musicIcon = computed(() => (music: Music) => music.id === musicHoveringId.value ? mdiPlay : mdiFileMusicOutline)

withDefaults(defineProps<{ depth?: number }>(), {
    depth: 0
});
const musicFolder = defineModel({ type: {} as PropType<Folder>, required: true });

const hasContent = computed(() => musicFolder.value.musics.length || musicFolder.value.folders.length);

function startPlay(music: Music) {
    playlist.setCurrentPlaying(music);
}

</script>