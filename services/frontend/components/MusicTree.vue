<template>
    <v-list>
        <MusicTreeGroup v-model="musicFolder" />
    </v-list>
</template>
<script setup lang="ts">
import type { Folder } from '~/commons/interfaces';
import MusicTreeGroup from './MusicTreeGroup.vue';
const musicFolder = defineModel({ type: {} as PropType<Folder>, required: true });
</script>