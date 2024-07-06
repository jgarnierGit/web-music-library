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
        <ArtistsCards />
      </v-sheet>
    </v-col>
  </v-row>
</template>
<script setup lang="ts">
import ArtistsCards from '~/components/artist/ArtistsCards.vue';
import MusicTree from '~/components/filesystem/MusicTree.vue';
</script>
