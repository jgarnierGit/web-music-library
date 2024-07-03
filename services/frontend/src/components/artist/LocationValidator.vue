<template>
    <v-row align="center" class="d-flex justify-space-evenly">
        <v-col>
            {{ countryName }}
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="4">
            <v-btn-toggle divided density="compact" variant="outlined">
                <v-btn size="x-small" color="success" @click="$emit('save', artist, countryName)">
                    <v-icon end color="success">
                        {{ mdiContentSaveEdit }}
                    </v-icon>
                </v-btn>
            </v-btn-toggle>
        </v-col>
    </v-row>
</template>

<script setup lang="ts">
import { mdiContentSaveEdit } from '@mdi/js';
import type { Artist } from '~/commons/interfaces';
defineProps<{
    countryName: string, artist: Artist
}>();

const emit = defineEmits(['save', 'cancel']);

</script>