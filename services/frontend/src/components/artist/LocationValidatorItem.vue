<template>
    {{ countryName ?? 'NO DATA' }}
    <v-btn-toggle divided density="compact" variant="outlined">
        <v-btn size="x-small" color="success" @click="$emit('save', artist, countryName)" :disabled="!countryName">
            <v-icon end color="success">
                {{ mdiContentSaveEdit }}
            </v-icon>
        </v-btn>
        <v-btn size="x-small" color="error" @click="$emit('cancel', artist)">
            <v-icon end color="error">
                {{ mdiContentSaveOff }}
            </v-icon>
        </v-btn>
    </v-btn-toggle>
</template>
<script setup lang="ts">
import { mdiContentSaveEdit, mdiContentSaveOff } from '@mdi/js';
import type { Artist } from '~/commons/interfaces';

defineProps<{
    countryName?: string, artist: Artist
}>();
const emit = defineEmits(['save', 'cancel']);

</script>