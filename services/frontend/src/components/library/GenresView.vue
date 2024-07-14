<template>
    <LibraryContentView title="Genres" :countLoaded="countLoadedGenres" :refreshCountCallback="refreshCount"
        :autoRefresh="true" :dataPending="dataPending" :dataError="dataError">
        <ListContent v-if="!isCard" :load="load" v-slot="{ content, hoveringId }" :contents="genresData">
            <v-list-item :title="`${typedContent(content).name}`">
                <v-list-item-subtitle class="content-list-item">
                    <button @click="artistsView()">{{ typedContent(content).artists_count }}
                        artists</button>
                    <v-divider></v-divider>
                    <v-chip @click="yearsView(date)" color="primary" size="small" variant="outlined" density="compact"
                        v-for="date in typedContent(content).dates">
                        {{ date }}
                    </v-chip>
                </v-list-item-subtitle>
                <template v-slot:prepend>
                    <v-icon v-if="hoveringId != typedContent(content).id">{{ mdiAccount }}</v-icon>
                    <PlaylistActions v-else :type="PLAYLIST_TYPES.GENRE" :value="[typedContent(content).id]" />
                </template>
            </v-list-item>
        </ListContent>
        <CardContent v-else :load="load" v-slot="{ content, isHovering }" :contents="genresData">
            <v-img src="/default_artist.png" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>
                <v-card-title class="text-h6 content-card-title">
                    {{ typedContent(content).name }}
                </v-card-title>
                <v-card-text class="content-card-bottom ma-0 pa-0">
                    <p class="text-caption font-weight-medium">
                        <button @click="artistsView()">{{ typedContent(content).artists_count }}
                            artists</button>
                    </p>
                    <v-card-actions :class="[{ 'hide-playlist-actions': !isHovering }, 'justify-center']">
                        <PlaylistActions :type="PLAYLIST_TYPES.GENRE" :value="[typedContent(content).id]" variant="text"
                            density="default" />
                    </v-card-actions>
                </v-card-text>
            </v-img>
        </CardContent>
    </LibraryContentView>
</template>

<script setup lang="ts">
import { getAPI, writeInfoLogs } from '~/commons/restAPI';
import type { ContentList, Genre } from '~/commons/interfaces';
import { PLAYLIST_TYPES } from '~/commons/constants';
import { mdiAccount } from '@mdi/js';
import LibraryContentView from './LibraryContentView.vue';
import ListContent from './ListContent.vue';
import CardContent from './CardContent.vue';
import PlaylistActions from '../PlaylistActions.vue';
const dbCacheStore = useDbCacheStore();
const { genresData, countLoadedGenres } = storeToRefs(dbCacheStore);
const fileSystemStore = useFilesystemStore();
const { isCard } = storeToRefs(fileSystemStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('albumsListData', () => loadContents());

const typedContent = computed(() => (content: any) => content as Genre)

watch(genresData, (newVal) => {
    if (newVal) {
        // mapStore.updateLayerData(createGeomData(albumsData.value.contents.filter((album: Album) => artist.geom)));
        // TODO update geom by artists linked to album?
    }
});

async function loadContents() {
    if (genresData.value) {
        writeInfoLogs("skip genres refresh");
        return
    }

    return await reloadContents();
}

async function reloadContents() {
    dataPending.value = true;
    const res = await getAPI(`/api/genres/list`, 'loading genres list');

    if (!res) {
        return;
    }
    dbCacheStore.setGenresData({ contents: res.contents } as ContentList<Genre>);
    dataPending.value = false;
    return res
}

//@ts-ignore
async function load({ done }) {
    const res: any = await getAPI(`/api/genres/list?offset=${genresData.value.contents.length}`, 'loading more genres');
    if (res.contents && res.contents.length > 0) {
        genresData.value.contents.push(...res.contents);
        done('ok')
    }
    else {
        done('empty')
    }
}


async function refreshCount() {
    const res = await getAPI(`/api/genres/count`, 'refresh genres count');
    if (!res) {
        return "No data";
    }
    return res.result;
}
function artistsView() {
    console.log("genre artists");
}

function yearsView(year: number) {
    console.log("genre years");
}


</script>

<style>
.badge-toolbar {
    pointer-events: none !important;
}

.content-card-title {
    text-wrap: stable;
    opacity: 1 !important;
    text-align: center;
}

.content-card-bottom {
    position: absolute;
    bottom: 0;
    width: 100%;
    text-align: center;

    button:hover {
        text-decoration: underline;
    }
}

.hide-playlist-actions {
    visibility: hidden;
}

.content-list-item {
    button:hover {
        text-decoration: underline;
    }
}
</style>