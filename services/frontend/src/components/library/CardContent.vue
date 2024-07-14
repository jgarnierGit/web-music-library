<template>
    <v-infinite-scroll :height="300" :items="contents.contents" :onLoad="load">
        <v-container fluid>
            <v-row dense justify="start">
                <template cols="3" v-for="content in contents.contents" :key="content.id">
                    <v-hover v-slot="{ isHovering, props }">
                        <v-card width="10vw" height="10vw" min-width="200px" min-height="200px"
                            :class="[{ 'on-hover': isHovering }, 'd-flex', 'flex-column', 'text-white', 'ma-1']"
                            :elevation="isHovering ? 12 : 2" v-bind="props">
                            <slot :content="content" :isHovering="isHovering"></slot>
                        </v-card>
                    </v-hover>
                </template>
            </v-row>
        </v-container>
    </v-infinite-scroll>
</template>
<script setup lang="ts" generic="T extends Album| Artist| Genre| Year">
import type { Album, Artist, ContentList, Genre, Year } from '~/commons/interfaces';

defineProps<{ load: any, contents: ContentList<T> }>()

</script>
