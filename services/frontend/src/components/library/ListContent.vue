<template>
    <v-infinite-scroll :height="300" :items="contents.contents" item-height="48" @load="load">
        <template v-for="(content, index) in contents.contents" :key="content.id">
            <span v-on:mouseenter="hoveringContentId = content.id" v-on:mouseleave="hoveringContentId = undefined">
                <slot :content="content" :hoveringId="hoveringContentId">
                </slot>
            </span>
        </template>
    </v-infinite-scroll>
</template>

<script setup lang="ts" generic="T extends Album| Artist| Genre| Year">
import type { Album, Artist, ContentList, Genre, Year } from '~/commons/interfaces';

defineProps<{ load: any, contents: ContentList<T> }>()
const hoveringContentId = ref();
function sayHey() {
    console.log('yo')
}
</script>
