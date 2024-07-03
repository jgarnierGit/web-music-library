<template>
    <v-navigation-drawer model-value expand-on-hover rail>
        <v-list density="compact" nav>
            <v-list-item :prepend-icon="mdiFolderPlay" title="Navigator" value="navigator" @click="goHome()">
                <v-tooltip activator="parent" location="end">Find & Play</v-tooltip>
            </v-list-item>
            <v-list-item :prepend-icon="mdiMapMarkerRadius" title="Artists Geolocalizer" value="geolocalizer"
                @click="goGeoEditor()">
                <v-tooltip activator="parent" location="end">Open editor</v-tooltip>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item :prepend-icon="mdiRadar" title="Scan your music" value="scan">
                <v-tooltip activator="parent" location="end">Refresh from filesystem</v-tooltip>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>

<script setup lang="ts">
import { mdiFolderPlay, mdiMapMarkerRadius, mdiRadar } from '@mdi/js';

function goHome() {
    navigateTo("/");
}

function goGeoEditor() {
    navigateTo("/geolocalizer");
}
</script>