<template>
  <v-row>
    <v-col>
      <v-sheet rounded="lg">
        <ArtistsGeolocalizer />
      </v-sheet>
    </v-col>
    <v-col cols="7" class="opacity-100">
      <InteractiveMap />
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
import InteractiveMap from '~/components/InteractiveMap.vue';
import ArtistsGeolocalizer from '~/components/artist/ArtistsGeolocalizer.vue';

</script>