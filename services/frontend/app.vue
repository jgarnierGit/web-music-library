<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
const demoLoaded = ref(false);
const projectMLoaded = ref(false);
watch([demoLoaded, projectMLoaded], ([newA, newB]) => {
  if (!!newA && !!newB) {
    loadModule()
  }
})
useHead({
  script: [
    {
      src: 'projectm/projectm.js', defer: true, async: true, onload: () => projectMLoaded.value = true
    },
    {
      src: 'projectm/demo.js', defer: true, async: true, onload: () => demoLoaded.value = true
    }]
});
</script>
