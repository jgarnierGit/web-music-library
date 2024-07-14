<template>
    <ArtistsView v-if="activeNavigatorView.target === 'Artists'" />
    <AlbumsView v-else-if="activeNavigatorView.target === 'Albums'" />
    <GenresView v-else-if="activeNavigatorView.target === 'Genres'" />
    <YearsView v-else-if="activeNavigatorView.target === 'Years'" />
</template>

<script setup lang="ts">
import ArtistsView from './library/ArtistsView.vue';
import AlbumsView from './library/AlbumsView.vue';
import GenresView from './library/GenresView.vue';
import YearsView from './library/YearsView.vue';
const fileSystemStore = useFilesystemStore();

const { activeNavigatorView } = storeToRefs(fileSystemStore);

</script>