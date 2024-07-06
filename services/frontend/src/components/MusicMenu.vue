<template>
    <v-navigation-drawer model-value expand-on-hover rail @update:rail="updateRailEvent">
        <v-list density="compact" nav>
            <v-list-item :prepend-icon="mdiFolderPlay" title="Navigator" value="navigator" @click="goHome()"
                variant="tonal">
                <v-tooltip activator="parent" location="end">Find & Play</v-tooltip>
            </v-list-item>
            <v-list-item :prepend-icon="mdiMapMarkerRadius" title="Artists Geolocalizer" value="geolocalizer"
                @click="goGeoEditor()" variant="tonal">
                <v-tooltip activator="parent" location="end">Open editor</v-tooltip>
            </v-list-item>
            <v-divider></v-divider>
            <RefreshFileSystem :rail="railRetracted" />
        </v-list>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { mdiFolderPlay, mdiMapMarkerRadius } from '@mdi/js';
import RefreshFileSystem from './RefreshFileSystem.vue';
const railRetracted = ref(true);

function goHome() {
    navigateTo("/");
}

function goGeoEditor() {
    navigateTo("/geolocalizer");
}

function updateRailEvent(e: any) {
    railRetracted.value = e;
}

</script>