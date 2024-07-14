<template>
    <v-card>
        <NavigatorDropdownToolbar :title="title" :countLoaded="countLoaded" :countRefreshCallback="refreshCountCallback"
            :autoRefresh="autoRefresh" toolbarContextId="-library">
            <v-btn v-if="!isCard" @click="fileSystemStore.switchIsCard()"><v-icon>{{ mdiAccountBoxOutline }}</v-icon>
                <v-tooltip activator="parent" location="top">Display as cards</v-tooltip>
            </v-btn>
            <v-btn v-else @click="fileSystemStore.switchIsCard()"><v-icon>{{ mdiFormatListText }}</v-icon>
                <v-tooltip activator="parent" location="top">Display in list</v-tooltip></v-btn>
        </NavigatorDropdownToolbar>
        <v-container fluid v-if="dataPending">
            <v-row dense justify="start">
                <v-col cols="3" v-for="n in 3">
                    <v-skeleton-loader :type="isCard ? 'card' : 'list-item'"></v-skeleton-loader>
                </v-col>
            </v-row>
        </v-container>
        <v-container fluid v-else-if="dataError">
            <v-alert density="compact" :icon="mdiCloseCircle" color="error" variant="outlined">
                {{ title }} access error ...
                <v-divider color="error"></v-divider>
                Server log: "{{ dataError }}"
            </v-alert>
        </v-container>
        <slot v-else></slot>
    </v-card>
</template>

<script setup lang="ts">
import { mdiAccountBoxOutline, mdiCloseCircle, mdiFormatListText } from '@mdi/js';
import NavigatorDropdownToolbar from './NavigatorDropdownToolbar.vue';
defineProps<{ title: string, countLoaded: number, refreshCountCallback: () => Promise<any>, autoRefresh: boolean, dataPending: boolean, dataError?: any }>()
const fileSystemStore = useFilesystemStore();
const { isCard } = storeToRefs(fileSystemStore);

</script>

<style>
.badge-toolbar {
    pointer-events: none !important;
}
</style>