<template>
    <div id="container"></div>
</template>
<script setup lang="ts">

onMounted(() => {
    toggleVisualizer();
})

onBeforeUnmount(() => {
    destruct();
})
</script>

<style>
#container {
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    z-index: -1;
    background: initial;
}
</style>