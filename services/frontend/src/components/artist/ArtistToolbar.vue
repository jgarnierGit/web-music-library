<template>
    <v-toolbar density="compact">
            <v-toolbar-title>Artists
                <v-badge v-if="!countPending" :content="artistsCount.result" inline />
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-toolbar-items>
                <v-btn icon v-if="countPending" variant="text" readonly>
                    <v-progress-circular :size="20" :width="2" indeterminate></v-progress-circular>
                </v-btn>
            </v-toolbar-items>
        </v-toolbar>
    </template>

    <script setup lang="ts">
import { getAPI } from '~/commons/restAPI';

    const { pending: countPending, data: artistsCount } = await useLazyAsyncData('artistsListCount', () => getAPI(`/api/artist/count`, 'counting artists'));

    </script>