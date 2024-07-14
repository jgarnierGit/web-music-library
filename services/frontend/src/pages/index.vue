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
        <LibraryView />
      </v-sheet>
    </v-col>
  </v-row>
</template>
<script setup lang="ts">
import LibraryView from '~/components/LibraryView.vue';
import MusicTree from '~/components/filesystem/MusicTree.vue';
</script>
