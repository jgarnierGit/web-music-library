<template>
  <v-row class="background-opacity-90">
    <v-col>
      <v-sheet rounded="lg">
        <Artists v-model="mockArtists" />
      </v-sheet>
      <v-sheet rounded="lg">
        <MusicTree v-model="library" class="overflow-y-auto" max-height="90vh" />
      </v-sheet>
    </v-col>
    <v-col cols="8" class="opacity-100">
      <InteractiveMap />
    </v-col>

  </v-row>
</template>
<script setup lang="ts">
import { reactive } from 'vue';
import type { Folder } from '~/commons/interfaces';
import MusicTree from '~/components/MusicTree.vue';
import Artists from '~/components/Artists.vue';



const content: Folder = { id: '', name: '', folders: [], musics: [], path: '' };


const mockArtists = reactive({ "artists": [{ "id": "55a984eb-9306-4cdd-b5b2-c10675425bad", "name": "fake_artist", "country_name": null, "geom": null }] });


const library = reactive(content);
</script>
<style>
.background-opacity-90 {
  background-color: rgba(238, 238, 238, 0.9)
}
</style>
