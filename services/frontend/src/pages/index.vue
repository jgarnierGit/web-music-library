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
            <Artists />
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
import Artists from '~/components/Artists.vue';
import InteractiveMap from '~/components/InteractiveMap.vue';
import MusicTree from '~/components/MusicTree.vue';


</script>
