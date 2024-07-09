<template>
    <v-card>
        <NavigatorToolbar title="Geolocalizer" :countLoaded="countLoadedData"
            :countRefreshCallback="refreshArtistGeoms" />
        <v-sheet height="70vh" max-height="90vh" rounded="lg">
            <div id="musicMap" class="mapContainer">
            </div>
            <div ref="mapPlayerButton">
                Play from
                <v-divider></v-divider>
                <span v-for="country in activeCountryPopup">{{ country }}<br /></span>
                <PlaylistActions :type="PLAYLIST_TYPES.COUNTRY" :value="activeCountryPopup" />
            </div>
        </v-sheet>
    </v-card>
</template>
<script setup lang="ts">
import 'leaflet/dist/leaflet.css';
import shp from 'shpjs';
import * as turf from '@turf/turf';
import L from 'leaflet';
import "leaflet.markercluster";
import type { GeomData } from '~/commons/interfaces';
import { COUNTRY_FIELD_NAME, FRONT_PUBLIC_URL, PLAYLIST_TYPES } from '~/commons/constants';
import { getAPI, writeErrorLogs, writeInfoLogs } from '~/commons/restAPI';
import PlaylistActions from './PlaylistActions.vue';
import { createGeomData } from '~/commons/utils';

const activeCountryPopup = ref<string[]>([]);
const countLoadedData = ref(0);
const mapStore = useSpatialMapStore();
const playlist = usePlaylistStore();
const dbCacheStore = useDbCacheStore();
const { editionId, editorContext, geomLayerData, countriesFeatures, countriesLayer } = storeToRefs(mapStore);
const style = {
    hilight: {
        dashArray: '',
        fillColor: 'white',
        fillOpacity: 0.85
    },
    default: {
        fillOpacity: 0, weight: 1,
        color: 'black',
    }
}

await useAsyncData('countries', () => loadCountries());
const mapPlayerButton = ref();
const layersCountValues = ref();
const clusterPopupPlayer = ref();
const editionMarker = shallowRef();
const countryTooltip = shallowRef();
const ArtistTooltip = shallowRef();
const readMarkers = shallowRef();
const activeReadCountries = shallowRef<any[]>([]);
// avoid zoom side effect on leaftlet map events (un)binding one could have using regular ref()
const leafletMap = shallowRef<L.Map>()

watch(editionId, (newVal) => {
    if (!newVal) {
        if (geomLayerData.value) {
            createReadMarkers(geomLayerData.value);
        }
        if (editionMarker.value) {
            editionMarker.value.remove();
            editionMarker.value = undefined;
        }
    }
    else {
        readMarkers.value.remove();
    }
});

watch(geomLayerData, (newVal, oldVal) => {
    if (newVal && newVal.length > 0) {
        layersCountValues.value = newVal.reduce((all: any, value: GeomData) => {
            all[value.name] = (all[value.name] ?? 0) + 1;
            return all;
        }, {});
        countLoadedData.value = newVal.length;
        createReadMarkers(newVal);
    }
})

watch([countriesFeatures, leafletMap], ([newValLayer, newValMap]) => {
    if (newValLayer && newValMap) {
        const cLayer = L.geoJSON(newValLayer, {
            style: style.default,
            onEachFeature: onEachFeature
        });
        cLayer.addTo(newValMap);
        mapStore.setCountriesLayer(cLayer);
        L.Icon.Default.prototype.options.className = "mapMarker";
        if (geomLayerData.value) {
            createReadMarkers(geomLayerData.value)
        }
    }
},
    { immediate: true });

async function refreshArtistGeoms() {
    const res = await getAPI(`/api/map/getGeometries`, 'fetch artist geoms');
    if (!res) {
        return "No data";
    }
    countLoadedData.value = res.result.length;
    mapStore.updateLayerData(createGeomData(res.result));
    dbCacheStore.setArtistDataGeomOnly(res.result);
    return res.result.length;
}

function createReadMarkers(data: GeomData[]) {
    if (!leafletMap.value) {
        console.log("Map is not initiated, couldn't add markers");
        return;
    }
    if (!readMarkers.value) {
        readMarkers.value = L.markerClusterGroup({ animateAddingMarkers: true, showCoverageOnHover: false });
        readMarkers.value.on('mouseover', (a: any) => hilightCountryFromReadMarker(a));
        readMarkers.value.on('mouseout', (a: any) => resetCountryStyleReadMarker(a));
        readMarkers.value.on('click', setActiveCountry);
        readMarkers.value.on('clusterclick', function (a: any) {
            clusterPopupPlayer.value = L.popup()
                .setLatLng(a.layer.getLatLng())
                .setContent(mapPlayerButton.value)
                //@ts-ignore
                .openOn(leafletMap.value);
            setActiveCountry(a);
        });
        readMarkers.value.on('clustermouseover', function (a: any) {
            hilightCoutriesReaderCluster(a);
        });
        readMarkers.value.on('clustermouseout', function (a: any) {
            resetCountryStyleReadMarker(a);
        });
    }
    readMarkers.value.clearLayers();
    const markersList = data.map((geoData: GeomData) => {
        //TODO find a way to replace title with a tooltip
        return L.marker([geoData.geom.coordinates[0], geoData.geom.coordinates[1]], { title: geoData.feature_name }).bindPopup(mapPlayerButton.value)

    })
    readMarkers.value.addLayers(markersList);
    if (!leafletMap.value.hasLayer(readMarkers.value)) {
        leafletMap.value.addLayer(readMarkers.value);
    }

}

function setActiveCountry(a: any) {
    const activeCountries = activeReadCountries.value.map((layer) => layer.feature.properties[COUNTRY_FIELD_NAME]);
    if (activeCountries.length === 1) {
        activeCountryPopup.value = activeCountries
    } else {
        activeCountryPopup.value = activeCountries
        writeErrorLogs("multi countries filtering not handled yet");
    }
}

function hilightCoutriesReaderCluster(a: any) {
    const testConvexHull = new L.Polygon(a.layer.getConvexHull())
    const latLngs = testConvexHull.getLatLngs() as L.LatLng[][];
    if (!!a.target._spiderfied || latLngs[0].length === 1) {
        // is a point cluster
        hilightCountryFromReadMarker(a);
    }
    else {
        const coords = latLngs[0].map((latLng: any) => [latLng.lng, latLng.lat]);
        if (latLngs[0].length === 2) {
            const turfPolygon = turf.lineString(coords);
            countriesLayer.value.eachLayer(function (layer: any) {
                if (turf.lineIntersect(turfPolygon, layer.feature).features.length > 0) {
                    activeReadCountries.value.push(layer)
                    layer.setStyle(style.hilight);
                }
            });
        } else {
            // is a polygon cluster
            // make it circular to respect turf convention.
            coords.push(coords[0]);
            const turfPolygon = turf.polygon([coords]);
            countriesLayer.value.eachLayer(function (layer: any) {
                const countData = layersCountValues.value[layer.feature.properties[COUNTRY_FIELD_NAME]] ?? 0;
                if (countData > 0 && turf.booleanIntersects(turfPolygon, layer.feature)) {
                    activeReadCountries.value.push(layer)
                    layer.setStyle(style.hilight);
                }
            });
        }
    }
}

function hilightCountryFromReadMarker(a: any) {
    if (!!a.layer._spiderLeg) {
        // if is the current cluster being spiderfied, then get root latLng
        const latlngOrigin = a.target._spiderfied.getLatLng();
        const p = turf.point([latlngOrigin.lng, latlngOrigin.lat]);
        countriesLayer.value.eachLayer(function (layer: any) {
            const isIntersecting = turf.booleanPointInPolygon(p, layer.feature);
            if (isIntersecting) {
                activeReadCountries.value.push(layer)
                layer.setStyle(style.hilight);
            }
        });
    }
    else {
        const p = turf.point([a.latlng.lng, a.latlng.lat]);
        countriesLayer.value.eachLayer(function (layer: any) {
            const isIntersecting = turf.booleanPointInPolygon(p, layer.feature);
            if (isIntersecting) {
                activeReadCountries.value.push(layer)
                layer.setStyle(style.hilight);
                const targetedArtists = geomLayerData.value?.filter((geomData: GeomData) => geomData.name === layer.feature.properties[COUNTRY_FIELD_NAME]);
                if (!targetedArtists) {
                    return
                }
                if (targetedArtists.length === 1) {
                    ArtistTooltip.value = L.tooltip()
                        .setLatLng(a.latlng)
                        .setContent(targetedArtists[0].feature_name)
                        //@ts-ignore
                        .addTo(leafletMap.value);
                }
            }
        });
    }
}

function resetCountryStyleReadMarker(a: any) {
    activeReadCountries.value.forEach((layer) => countriesLayer.value.resetStyle(layer));
    activeReadCountries.value = [];
    if (ArtistTooltip.value) {
        ArtistTooltip.value.remove();
    }
}

onMounted(() => {
    initLeafletMap();
})

function initLeafletMap() {
    leafletMap.value = L.map('musicMap', { maxBoundsViscosity: 1 }).setView([53, 12], 2);
    L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg', {
        minZoom: 1,
        maxZoom: 10,
        attribution: '&copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
    }).addTo(leafletMap.value);
}


async function loadCountries() {
    if (countriesLayer.value) {
        writeInfoLogs("Skip countries shp loading");
        return
    }
    const shpRes = await shp(`${FRONT_PUBLIC_URL}/geodata/ne_110m_admin_0_countries`);
    mapStore.setCountriesFeatures(shpRes);
}

function onEachFeature(feature: any, layer: any) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: pickCountry
    })
}

function highlightFeature(e: any) {
    let layer = e.target;
    layer.setStyle(style.hilight);
    if (!leafletMap.value) {
        return
    }
    if (!!editionId.value) {
        countryTooltip.value = L.tooltip()
            .setLatLng(e.latlng)
            .setContent(e.target.feature.properties[COUNTRY_FIELD_NAME])
            .addTo(leafletMap.value);
    } else if (!editionId.value && layersCountValues.value && layersCountValues.value[e.target.feature.properties[COUNTRY_FIELD_NAME]]) {
        countryTooltip.value = L.tooltip()
            .setLatLng(e.latlng)
            .setContent(`Play from ${e.target.feature.properties[COUNTRY_FIELD_NAME]}`)
            .addTo(leafletMap.value);
    }
}

function resetHighlight(e: any) {
    countriesLayer.value.resetStyle(e.target);
    if (countryTooltip.value && leafletMap.value) {
        countryTooltip.value.remove();
    }
}

async function pickCountry(event: any) {
    if (!editionId.value) {
        await playlist.setFilter(PLAYLIST_TYPES.COUNTRY, [event.target.feature.properties[COUNTRY_FIELD_NAME]]);
        playlist.playNextSong();
        return;
    }
    updateEditionMarker(event);
    editorContext.value?.callback({ countryName: editionMarker.value.options.title, geom: editionMarker.value.centroid.geometry });
}

function markerMouseOver(e: any) {
    countriesLayer.value.eachLayer((layer: any) => {
        if (layer.feature === editionMarker.value.feature) {
            layer.setStyle(style.hilight);
        }
    })
}

function markerMouseOut(e: any) {
    countriesLayer.value.eachLayer((layer: any) => {
        if (layer.feature === editionMarker.value.feature) {
            layer.setStyle(style.default);
        }
    })
}

function updateEditionMarker(event: any) {
    if (!leafletMap.value) {
        console.error("Map is not instanciated yet");
        return;
    }
    var clickCoordInvert = { lat: event.latlng.lng, lng: event.latlng.lat }
    const pickedPolygon: L.Polygon<any> = event.target.feature.geometry.coordinates
        .map((polygonCoords: any) => L.polygon(polygonCoords))
        .find((subPolygon: L.Polygon<any>) =>
            subPolygon.getBounds().contains(clickCoordInvert)
        );
    if (!pickedPolygon) {
        return;
    }
    const centroid = turf.centerOfMass(pickedPolygon.toGeoJSON())
    const countryName = event.target.feature.properties[COUNTRY_FIELD_NAME];
    const centroidLatLong = new L.LatLng(centroid.geometry.coordinates[0], centroid.geometry.coordinates[1]);
    if (!editionMarker.value) {
        editionMarker.value = L.marker(centroidLatLong, { title: countryName });
        editionMarker.value.addTo(leafletMap.value)
        editionMarker.value.on({
            // hilight feature to disambiguate marker parenting
            mouseover: markerMouseOver,
            mouseout: markerMouseOut
        })
    } else {
        editionMarker.value.options.title = countryName;
        editionMarker.value.setLatLng(centroidLatLong);
    }
    editionMarker.value.feature = event.target.feature;
    editionMarker.value.centroid = centroid;
}
</script>

<style>
.mapContainer {
    width: 100%;
    height: 100%;

    opacity: 1 !important;
}

.mapMarker {
    filter: grayscale(100%) brightness(100%);
}
</style>