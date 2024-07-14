<template>
    <LibraryContentView title="Artists" :countLoaded="countLoadedArtists" :refreshCountCallback="refreshCount"
        :autoRefresh="true" :dataPending="dataPending" :dataError="dataError">
        <ListContent v-if="!isCard" :load="load" v-slot="{ content, hoveringId }" :contents="artistsData">
            <v-list-item :title="`${typedContent(content).name}`">
                <v-list-item-subtitle class="content-list-item">
                    <button @click="albumsView()">{{ typedContent(content).albums_count }} albums</button> - <button
                        @click="tracksView()">{{ typedContent(content).tracks_count }}
                        tracks</button>
                    <v-divider></v-divider>
                    <v-chip @click="genresView(genre.id)" color="primary" size="small" variant="outlined"
                        density="compact" v-for="genre in typedContent(content).genres">
                        {{ genre.name }}
                    </v-chip>
                </v-list-item-subtitle>
                <template v-slot:prepend>
                    <v-icon v-if="hoveringId != typedContent(content).id">{{ mdiAccount }}</v-icon>
                    <PlaylistActions v-else :type="PLAYLIST_TYPES.ARTIST" :value="[typedContent(content).id]" />
                </template>
            </v-list-item>
        </ListContent>
        <CardContent v-else :load="load" v-slot="{ content, isHovering }" :contents="artistsData">
            <v-img src="/default_artist.png" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" cover>
                <v-card-title class="text-h6 artist-card-title">
                    {{ typedContent(content).name }}
                </v-card-title>
                <v-card-text class="artist-card-bottom ma-0 pa-0">
                    <p class="text-caption font-weight-medium">
                        <button @click="albumsView()">{{ typedContent(content).albums_count }} albums</button> -
                        <button @click="tracksView()">{{ typedContent(content).tracks_count }}
                            tracks</button>
                    </p>
                    <v-card-actions :class="[{ 'hide-playlist-actions': !isHovering }, 'justify-center']">
                        <PlaylistActions :type="PLAYLIST_TYPES.ARTIST" :value="[typedContent(content).id]"
                            variant="text" density="default" />
                    </v-card-actions>
                </v-card-text>
            </v-img>
        </CardContent>
    </LibraryContentView>
</template>

<script setup lang="ts">
import type { Artist, ContentList } from '~/commons/interfaces';
import { getAPI, writeInfoLogs } from '~/commons/restAPI';
import { createGeomData } from '~/commons/utils';
import { PLAYLIST_TYPES } from '~/commons/constants';
import { mdiAccount } from '@mdi/js';
import LibraryContentView from './LibraryContentView.vue';
import ListContent from './ListContent.vue';
import CardContent from './CardContent.vue';
import PlaylistActions from '../PlaylistActions.vue';
const mapStore = useSpatialMapStore();
const dbCacheStore = useDbCacheStore();
const fileSystemStore = useFilesystemStore();
const { isCard } = storeToRefs(fileSystemStore);
const { artistsData, countLoadedArtists } = storeToRefs(dbCacheStore);
const { pending: dataPending, error: dataError } = await useLazyAsyncData('artistsListData', () => loadArtists());
const typedContent = computed(() => (content: any) => content as Artist)

watch(artistsData, (newVal) => {
    if (newVal) {
        mapStore.updateLayerData(createGeomData(artistsData.value.contents.filter((artist: Artist) => artist.geom)));
    }
});

async function loadArtists() {
    if (artistsData.value) {
        writeInfoLogs("skip artist refresh");
        return
    }

    return await reloadArtists();
}

async function reloadArtists() {
    dataPending.value = true;
    const res = await getAPI(`/api/artists/list`, 'loading artists list');

    if (!res) {
        return;
    }
    mapStore.updateLayerData(createGeomData(res.contents.filter((artist: Artist) => artist.geom)));
    dbCacheStore.setArtistsData({ contents: res.contents } as ContentList<Artist>);
    dataPending.value = false;
    return res
}

//@ts-ignore
async function load({ done }) {
    const res: any = await getAPI(`/api/artists/list?offset=${artistsData.value.contents.length}`, 'loading more artists');
    if (res.contents && res.contents.length > 0) {
        artistsData.value.contents.push(...res.contents);
        done('ok')
    }
    else {
        done('empty')
    }
}


async function refreshCount() {
    const res = await getAPI(`/api/artists/count`, 'refresh artists count');
    if (!res) {
        return "No data";
    }
    return res.result;
}

function albumsView() {
    console.log("album");
}

function tracksView() {
    console.log("songs");
}

function genresView(id: string) {
    console.log("artist genre");
}

</script>

<style>
.badge-toolbar {
    pointer-events: none !important;
}

.artist-card-title {
    text-wrap: stable;
    opacity: 1 !important;
    text-align: center;
}

.artist-card-bottom {
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
</style>