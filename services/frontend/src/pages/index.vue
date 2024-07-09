<template>
  <v-row>
    <v-col>
      <v-sheet rounded="lg">
        <MusicTree />
      </v-sheet>
    </v-col>
  </v-row>
  <v-row>
    <v-col>
      <v-sheet rounded="lg">
        <ArtistsView />
      </v-sheet>
    </v-col>
  </v-row>
</template>
<script setup lang="ts">
import ArtistsView from '~/components/ArtistsView.vue';
import MusicTree from '~/components/filesystem/MusicTree.vue';
</script>
