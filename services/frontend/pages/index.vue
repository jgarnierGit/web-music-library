<template>
  <v-row>
    <v-col>
      <v-row>
        <v-col>
          <v-sheet rounded="lg">
            <MusicTree v-model="library" class="overflow-y-auto" max-height="80vh" />
          </v-sheet>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <v-sheet rounded="lg">
            <Artists v-model="mockArtists" />
          </v-sheet>
        </v-col>
      </v-row>
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


const mockArtists = reactive({
  "artists": [
    {
      "id": "98a0595d-428f-4a15-ba55-60953383113b",
      "name": "fake_artist",
      "country_name": null,
      "geom": null,
      "last_played": null,
      "count_played": 0,
      "count_skipped": 0
    }
  ]
});


const library = reactive(content);
</script>
