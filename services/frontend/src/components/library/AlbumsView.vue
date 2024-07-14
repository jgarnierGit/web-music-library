<template>
    <LibraryContentView title="Albums" :countLoaded="countLoadedAlbums" :refreshCountCallback="refreshCount"
        :autoRefresh="true" :dataPending="dataPending" :dataError="dataError">
        <ListContent v-if="!isCard" :load="load" v-slot="{ content, hoveringId }" :contents="albumsData">
            <v-list-item :title="`${typedContent(content).name}`">
                <v-list-item-subtitle class="content-list-item">
                    <button @click="tracksView()">{{ typedContent(content).tracks_count }}
                        tracks</button>
                    <v-divider></v-divider>
                    <v-chip @click="genresView(genre.id)" color="primary" size="small" variant="outlined"
                        density="compact" v-for="genre in typedContent(content).genres">
                        {{ genre.name }}
                    </v-chip>
                </v-list-item-subtitle>
                <template v-slot:prepend>
                    <v-icon v-if="hoveringId != typedContent(content).id">{{ mdiAccount }}</v-icon>
                    <PlaylistActions v-else :type="PLAYLIST_TYPES.ALBUM" :value="[typedContent(content).id]" />
                </template>
            </v-list-item>
        </ListContent>
        <CardContent v-else :load="load" v-slot="{ content, isHovering }" :contents="albumsData">
            <v-img src="/default_artist.png" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>
                <v-card-title class="text-h6 content-card-title">
                    {{ typedContent(content).name }}
                </v-card-title>
                <v-card-text class="content-card-bottom ma-0 pa-0">
                    <p class="text-caption font-weight-medium">
                        <button @click="tracksView()">{{ typedContent(content).tracks_count }}
                            tracks</button>
                    </p>
                    <v-card-actions :class="[{ 'hide-playlist-actions': !isHovering }, 'justify-center']">
                        <PlaylistActions :type="PLAYLIST_TYPES.ALBUM" :value="[typedContent(content).id]" variant="text"
                            density="default" />
                    </v-card-actions>
                </v-card-text>
            </v-img>
        </CardContent>
    </LibraryContentView>
</template>

<script setup lang="ts">
import { getAPI, writeInfoLogs } from '~/commons/restAPI';
import type { Album, ContentList } from '~/commons/interfaces';
import { PLAYLIST_TYPES } from '~/commons/constants';
import { mdiAccount } from '@mdi/js';
import LibraryContentView from './LibraryContentView.vue';
import ListContent from './ListContent.vue';
import PlaylistActions from '../PlaylistActions.vue';
import CardContent from './CardContent.vue';
const dbCacheStore = useDbCacheStore();
const { albumsData, countLoadedAlbums } = storeToRefs(dbCacheStore);
const fileSystemStore = useFilesystemStore();
const { isCard } = storeToRefs(fileSystemStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('albumsListData', () => loadContents());

const typedContent = computed(() => (content: any) => content as Album)

watch(albumsData, (newVal) => {
    if (newVal) {
        // mapStore.updateLayerData(createGeomData(albumsData.value.contents.filter((album: Album) => artist.geom)));
        // TODO update geom by artists linked to album?
    }
});

async function loadContents() {
    if (albumsData.value) {
        writeInfoLogs("skip albums refresh");
        return
    }

    return await reloadContents();
}

async function reloadContents() {
    dataPending.value = true;
    const res = await getAPI(`/api/albums/list`, 'loading albums list');

    if (!res) {
        return;
    }
    dbCacheStore.setAlbumsData({ contents: res.contents } as ContentList<Album>);
    dataPending.value = false;
    return res
}

//@ts-ignore
async function load({ done }) {
    const res: any = await getAPI(`/api/albums/list?offset=${albumsData.value.contents.length}`, 'loading more albums');
    if (res.contents && res.contents.length > 0) {
        albumsData.value.contents.push(...res.contents);
        done('ok')
    }
    else {
        done('empty')
    }
}


async function refreshCount() {
    const res = await getAPI(`/api/albums/count`, 'refresh albums count');
    if (!res) {
        return "No data";
    }
    return res.result;
}

function tracksView() {
    console.log("album songs");
}

function genresView(id: string) {
    console.log("album genre");
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