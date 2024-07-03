<template>
  <v-card>
    <ArtistToolbar />
    <v-container fluid v-if="dataPending">
      <v-row dense justify="start">
        <v-col cols="12" v-for="n in 3">
          <v-skeleton-loader type="list-item"></v-skeleton-loader>
        </v-col>
      </v-row>
    </v-container>
    <v-container fluid v-else-if="dataError">
      <v-alert density="compact" :icon="mdiCloseCircle" color="error" variant="outlined">
        Artists access error ...
        <v-divider color="error"></v-divider>
        Server log: "{{ dataError }}"
      </v-alert>
    </v-container>
    <v-infinite-scroll v-else height="80vh" item-height="48" :items="artistsData.artists" @load="load">
      <template v-for="(artist, index) in artistsData.artists" :key="artist.id">
        <v-list-item :subtitle="`${artist.country_name ?? 'NO DATA'}`" :title="`${artist.name}`">
          <template v-slot:prepend>
            <v-icon>{{ mdiAccount }}</v-icon>
          </template>

          <template v-slot:append>
            <div v-if="hasCountryGuessPending(artist.id)">
              <div v-if="hasArtistManyCountries(artist.id)">
                {{ artistCountryContent(artist.id)[0] ?? 'NO DATA' }}
                <v-btn-toggle divided density="compact" variant="outlined">
                  <v-btn size="x-small" variant="tonal">
                    (+{{ artistCountryContent(artist.id).length - 1 }} more...)
                    <v-icon color="warning" end>
                      {{ mdiOpenInNew }}
                    </v-icon>
                    <v-overlay activator="parent" location-strategy="connected" scroll-strategy="close"
                      v-model="overlay">
                      <v-card max-height="40vh" class="overflow-y-auto " max-width="20vw" min-width="15vw">
                        <v-list :items="artistCountryContent(artist.id)">
                          <v-list-item v-for="country in artistCountryContent(artist.id) ">
                            <LocationValidatorListItem :countryName="country" :artist="artist"
                              @save="saveGuessingLocation" @cancel="cancelGuessingLocation" />
                          </v-list-item>
                        </v-list>
                      </v-card>
                    </v-overlay>
                  </v-btn>
                  <v-btn size="x-small" color="error" @click="cancelGuessingLocation(artist)">
                    <v-icon end color="error">
                      {{ mdiContentSaveOff }}
                    </v-icon>
                  </v-btn>
                </v-btn-toggle>
              </div>
              <div v-else>
                <LocationValidatorItem :countryName="artistCountryContent(artist.id)[0]" :artist="artist"
                  @save="saveGuessingLocation" @cancel="cancelGuessingLocation" />
              </div>
            </div>
            <div v-else-if="editionId === artist.id">
              <LocationValidatorItem :countryName="editionContext.artist.country_name" :artist="artist"
                @save="switchEdition" @cancel="cancelEdition" />
            </div>
            <!-- no edition or guessing-->
            <div v-else>
              <v-tooltip location="top" origin="auto" text="Find location">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" :icon="mdiWeb" size="x-small" variant="tonal" @click="locate(artist)" />
                </template>
              </v-tooltip>
              <v-tooltip location="top" origin="auto" text="Edit on map">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" :icon="mdiPencil" size="x-small" variant="tonal"
                    @click="switchEdition(artist)"></v-btn>
                </template>
              </v-tooltip>
            </div>
          </template>
        </v-list-item>
      </template>
    </v-infinite-scroll>
  </v-card>
</template>

<script setup lang="ts">
import { mdiAccount, mdiCloseCircle, mdiContentSaveOff, mdiOpenInNew, mdiPencil, mdiWeb } from '@mdi/js';
import { getAPI, putAPI, writeErrorLogs } from '~/commons/restAPI';
import ArtistToolbar from './ArtistToolbar.vue';
import type { Artist, ArtistMapEditorContext } from '~/commons/interfaces';
import { createGeomData } from '~/commons/utils';
import { SNACKBAR_TIMEOUT } from '~/commons/constants';
import LocationValidatorListItem from './LocationValidatorListItem.vue';
import LocationValidatorItem from './LocationValidatorItem.vue';

const mapStore = useSpatialMapStore();
const geolocalizerStore = useGeolocalizerStore();
const snackbarStore = useSnackbarStore();
const { mappingRefCountries } = storeToRefs(geolocalizerStore);
const { editionId } = storeToRefs(mapStore);
const { pending: dataPending, data: artistsData, error: dataError } = await useLazyAsyncData('artistsListData', () => loadArtists());
const hasCountryGuessPending = computed(() => (artistId: string) => !!guessCountry.value[artistId]);
const hasArtistManyCountries = computed(() => (artistId: string) => guessCountry.value[artistId].length > 1);
const artistCountryContent = computed(() => (artistId: string) => guessCountry.value ? guessCountry.value[artistId] : "");

const guessCountry = ref({} as any);
const overlay = ref(false);
const editionContext = ref({} as ArtistMapEditorContext);

async function loadArtists() {
  const res = await getAPI(`/api/artist/list?limit=15`, 'loading artists list');
  if (!res) {
    return;
  }
  mapStore.updateLayerData(createGeomData(res.artists.filter((artist: Artist) => artist.geom)));
  return res;
}

//@ts-ignore
async function load({ done }) {
  const res: any = await getAPI(`/api/artist/list?offset=${artistsData.value.artists.length}`, 'loading more artists');
  if (res.artists && res.artists.length > 0) {
    artistsData.value.artists.push(...res.artists)
    mapStore.updateLayerData(createGeomData(res.artists.filter((artist: Artist) => artist.geom)));
    done('ok')
  }
  else {
    done('empty')
  }
}

async function locate(artist: Artist) {
  const res: any = await getAPI(`/api/artist/${artist.name}/getCountry`, `Getting country from artist ${artist.name}`)
  const artistId = artist.id;
  const labels = res.result.flatMap((val: string) => {
    //@ts-ignore
    const label = mappingRefCountries.value[val];
    if (!label) {
      writeErrorLogs(`unknown key country for ${val}`)
    }
    return label;
  });
  guessCountry.value[artistId] = labels;
}

async function saveGuessingLocation(artist: Artist, countryName: string) {
  if (!guessCountry.value[artist.id]) {
    return;
  }

  artist.country_name = countryName;
  const geom = mapStore.getGeomFromLabel(countryName);
  artist.geom = geom;
  mapStore.updateLayerData(createGeomData([artist]));
  await putAPI(`/api/artist/${artist.id}`, 'saving artist geolocalizer', artist);
  delete guessCountry.value[artist.id];
  overlay.value = false;
}

function cancelGuessingLocation(artist: Artist) {
  if (!guessCountry.value[artist.id]) {
    return;
  }
  delete guessCountry.value[artist.id];
}

async function switchEdition(artist: Artist) {
  if (editionId.value === artist.id) {
    mapStore.closeEditionId(artist.id);
    try {
      artist.country_name = editionContext.value.artist.country_name;
      artist.geom = editionContext.value.artist.geom;
      await putAPI(`/api/artist/${artist.id}`, 'saving artist', artist);
      mapStore.updateLayerData(createGeomData([artist]));
    } catch (err) {
      snackbarStore.setContent(`Error while loading saving artist ${artist.name}, check the logs`, SNACKBAR_TIMEOUT, "error");
      writeErrorLogs(`/api/artist/${artist.id} : ${err}`);
    }
    return;
  }
  else if (editionId.value) {
    mapStore.closeEditionId(editionId.value);
  }
  // opening edition for current artist

  editionContext.value.artist = {} as Artist;
  //TODO can be better typed using geomData
  editionContext.value.callback = (payload: { countryName: string, geom: any }) => {
    editionContext.value.artist.country_name = payload.countryName;
    editionContext.value.artist.geom = payload.geom;
  }
  mapStore.openEditionForId(artist.id, editionContext.value);
}

function cancelEdition(artist: Artist) {
  mapStore.closeEditionId(artist.id);
}

</script>