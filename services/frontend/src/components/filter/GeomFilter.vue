<template>
    <v-speed-dial location="left center" transition="slide-x-transition">
        <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-bind="activatorProps"><v-icon>{{ mdiFilterMenuOutline }}</v-icon></v-btn>
        </template>
        <v-btn :disabled="activeFilter === ACTIVE_GEOM_FILTER" @click="setFilter(ACTIVE_GEOM_FILTER)"
            :key="ACTIVE_GEOM_FILTER"><v-icon>{{
                mdiMapMarkerOutline }}</v-icon></v-btn>
        <v-btn :disabled="activeFilter === ACTIVE_NO_GEOM_FILTER" @click="setFilter(ACTIVE_NO_GEOM_FILTER)"
            :key="ACTIVE_NO_GEOM_FILTER"><v-icon>{{
                mdiMapMarkerOffOutline }}</v-icon></v-btn>
        <v-btn :disabled="!activeFilter" @click="setFilter(undefined)" key="resetFilter"><v-icon>{{
            mdiFilterOffOutline }}</v-icon></v-btn>

    </v-speed-dial>
</template>
<script setup lang="ts">
import { mdiFilterMenuOutline, mdiFilterOffOutline, mdiMapMarkerOffOutline, mdiMapMarkerOutline } from '@mdi/js';
import { ACTIVE_GEOM_FILTER, ACTIVE_NO_GEOM_FILTER } from '~/commons/constants';
const activeFilter = ref();

const emit = defineEmits(['updatefilter']);

function setFilter(val: string | undefined) {
    activeFilter.value = val;
    emit('updatefilter', val);
}

</script>