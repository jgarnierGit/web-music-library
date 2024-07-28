<template>
    <LibraryContentView title="Years" :countLoaded="countLoadedYears" :refreshCountCallback="refreshCount"
        :autoRefresh="true" :dataPending="dataPending" :dataError="dataError">
        <ListContent v-if="!isCard" :load="load" v-slot="{ content, hoveringId }" :contents="yearsData">
            <v-list-item :title="`${typedContent(content).date}`">
                <v-list-item-subtitle class="content-list-item">
                    <button @click="artistsView()">{{ typedContent(content).artists_count }}
                        artists</button>
                    <v-divider></v-divider>
                    <v-chip @click="genresView(genre.id)" color="primary" size="small" variant="outlined"
                        density="compact" v-for="genre in typedContent(content).genres">
                        {{ genre.name }}
                    </v-chip>
                </v-list-item-subtitle>
                <template v-slot:prepend>
                    <v-icon v-if="hoveringId != typedContent(content).id">{{ mdiAccount }}</v-icon>
                    <PlaylistActions v-else :type="PLAYLIST_TYPES.YEAR" :value="[`${typedContent(content).date}`]" />
                </template>
            </v-list-item>
        </ListContent>
        <CardContent v-else :load="load" v-slot="{ content, isHovering }" :contents="yearsData">
            <v-img src="/default_artist.png" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>
                <v-card-title class="text-h6 content-card-title">
                    {{ typedContent(content).date }}
                </v-card-title>
                <v-card-text class="content-card-bottom ma-0 pa-0">
                    <p class="text-caption font-weight-medium">
                        <button @click="artistsView()">{{ typedContent(content).artists_count }}
                            artists</button>
                    </p>
                    <v-card-actions :class="[{ 'hide-playlist-actions': !isHovering }, 'justify-center']">
                        <PlaylistActions :type="PLAYLIST_TYPES.YEAR" :value="[`${typedContent(content).date}`]"
                            variant="text" density="default" />
                    </v-card-actions>
                </v-card-text>
            </v-img>
        </CardContent>
    </LibraryContentView>
</template>

<script setup lang="ts">
import ListContent from './ListContent.vue';
import CardContent from './CardContent.vue';
import { mdiAccount } from '@mdi/js';
import { PLAYLIST_TYPES } from '~/commons/constants';
import type { ContentList, Year } from '~/commons/interfaces';
import { getAPI, writeInfoLogs } from '~/commons/restAPI';

const dbCacheStore = useDbCacheStore();
const { yearsData, countLoadedYears } = storeToRefs(dbCacheStore);
const fileSystemStore = useFilesystemStore();
const { isCard } = storeToRefs(fileSystemStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('yearsListData', () => loadContents());
const typedContent = computed(() => (content: any) => content as Year)

async function refreshCount() {
    const res = await getAPI(`/api/years/count`, 'refresh years count');
    if (!res) {
        return "No data";
    }
    return res.result;
}

async function loadContents() {
    if (yearsData.value) {
        writeInfoLogs("skip years refresh");
        return
    }

    return await reloadContents();
}

//@ts-ignore
async function load({ done }) {
    const res: any = await getAPI(`/api/years/list?offset=${yearsData.value.contents.length}`, 'loading more years');
    if (res.contents && res.contents.length > 0) {
        yearsData.value.contents.push(...res.contents);
        done('ok')
    }
    else {
        done('empty')
    }
}



async function reloadContents() {
    dataPending.value = true;
    const res = await getAPI(`/api/years/list`, 'loading years list');

    if (!res) {
        return;
    }
    dbCacheStore.setYearsData({ contents: res.contents } as ContentList<Year>);
    dataPending.value = false;
    return res
}

function artistsView() {
    console.log("years artists");
}

function genresView(id: string) {
    console.log("years genre");
}


</script>