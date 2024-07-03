<template>
  <v-card>
    <ArtistToolbar />
    <v-container fluid v-if="dataPending">
      <v-row dense justify="start">
        <v-col v-for="n in 3">
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
            <div v-if="!hasCountryGuessPending(artist.id)">
              <v-tooltip location="top" origin="auto" text="Find location">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" :icon="mdiMagnify" size="x-small" variant="tonal" @click="locate(artist)" />
                </template>
              </v-tooltip>
              <v-tooltip location="top" origin="auto" text="Edit on map">
                <template v-slot:activator="{ props }">
                  <v-btn v-bind="props" :icon="mdiPencil" size="x-small" variant="tonal"></v-btn>
                </template>
              </v-tooltip>
            </div>
            <div v-else>
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
                            <LocationValidator :countryName="country" :artist="artist" @save="saveLocation"
                              @cancel="cancelLocation" />
                          </v-list-item>
                        </v-list>
                      </v-card>
                    </v-overlay>
                  </v-btn>
                  <v-btn size="x-small" color="error" @click="cancelLocation(artist)">
                    <v-icon end color="error">
                      {{ mdiContentSaveOff }}
                    </v-icon>
                  </v-btn>
                </v-btn-toggle>
              </div>
              <div v-else>
                {{ artistCountryContent(artist.id)[0] ?? 'NO DATA' }}
                <v-btn-toggle divided density="compact" variant="outlined">
                  <v-btn size="x-small" color="success"
                    @click="saveLocation(artist, artistCountryContent(artist.id)[0])"
                    :disabled="!artistCountryContent(artist.id)[0]">
                    <v-icon end color="success">
                      {{ mdiContentSaveEdit }}
                    </v-icon>
                  </v-btn>
                  <v-btn size="x-small" color="error" @click="cancelLocation(artist)">
                    <v-icon end color="error">
                      {{ mdiContentSaveOff }}
                    </v-icon>
                  </v-btn>
                </v-btn-toggle>
              </div>
            </div>
          </template>
        </v-list-item>
      </template>
    </v-infinite-scroll>
  </v-card>
</template>

<script setup lang="ts">
import { mdiAccount, mdiCloseCircle, mdiContentSaveEdit, mdiContentSaveOff, mdiMagnify, mdiOpenInNew, mdiPencil } from '@mdi/js';
import { getAPI, putAPI, writeErrorLogs } from '~/commons/restAPI';
import ArtistToolbar from './ArtistToolbar.vue';
import type { Artist } from '~/commons/interfaces';
import LocationValidator from './LocationValidator.vue';
import { createGeomData } from '~/commons/utils';

const mapStore = useSpatialMapStore();
const geolocalizerStore = useGeolocalizerStore();
const { mappingRefCountries } = storeToRefs(geolocalizerStore);
const { pending: dataPending, data: artistsData, error: dataError } = await useLazyAsyncData('artistsListData', () => loadArtists());
const hasCountryGuessPending = computed(() => (artistId: string) => !!guessCountry.value[artistId]);
const hasArtistManyCountries = computed(() => (artistId: string) => guessCountry.value[artistId].length > 1);
const artistCountryContent = computed(() => (artistId: string) => guessCountry.value ? guessCountry.value[artistId] : "");
const guessCountry = ref({} as any);
const overlay = ref(false);

async function loadArtists() {
  const res = await getAPI(`/api/artist/list`, 'loading artists list');
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

async function saveLocation(artist: Artist, countryName: string) {
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

function cancelLocation(artist: Artist) {
  if (!guessCountry.value[artist.id]) {
    return;
  }
  delete guessCountry.value[artist.id];
}

</script>