<template>
  <v-app>
    <h1>
      {{ error?.statusCode }}
    </h1>
    {{ error?.message }}
    <NuxtLink to="/">
      Home page
    </NuxtLink>
  </v-app>
</template>

<script setup lang="ts">
import type { NuxtError } from '@nuxt/types';

const props = defineProps({
  error: Object as () => NuxtError
});

</script>
