<template>
    <MusicTree v-model="library" />
</template>
<script setup lang="ts">
import { reactive } from 'vue';
import type { Folder } from '~/commons/interfaces';
import MusicTree from '~/components/MusicTree.vue';

const content: Folder = { id: '', name: '', folders: [], musics: [], path: '' };
const library = reactive(content);
</script>