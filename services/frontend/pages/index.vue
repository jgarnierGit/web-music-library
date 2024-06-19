<template>
  <v-row>
    <v-col>
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
            <Artists v-model="mockArtists" />
          </v-sheet>
        </v-col>
      </v-row>
    </v-col>
    <v-col cols="4" class="opacity-100">
      <InteractiveMap />
    </v-col>

  </v-row>
</template>
<script setup lang="ts">
import { reactive } from 'vue';
import MusicTree from '~/components/MusicTree.vue';
import Artists from '~/components/Artists.vue';


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

</script>
