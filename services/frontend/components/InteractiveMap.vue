<template>
    <v-card>
        <v-toolbar density="compact">
            <v-toolbar-title>Geolocalizer
            </v-toolbar-title>
        </v-toolbar>
        <v-sheet height="70vh" max-height="90vh" rounded="lg">
            <div id="musicMap" class="mapContainer">
            </div>
        </v-sheet>
    </v-card>
</template>
<script setup lang="ts">
import 'leaflet/dist/leaflet.css';
import shp from 'shpjs';
import * as turf from '@turf/turf';
import { onMounted, ref } from 'vue'
import L from 'leaflet';
import "leaflet.markercluster";
import { FRONT_PUBLIC_URL } from '~/commons/constants';
import type { GeomData } from '~/commons/interfaces';

const countriesLayerBuffers = await useAsyncData('countries', () => loadCountries());
const countriesLayer = ref();
const mapStore = useSpatialMapStore();
const { editionId, editorContext, geomLayerData } = storeToRefs(mapStore);

const marker = ref();
// avoid zoom side effect on leaftlet map events (un)binding one could have using regular ref()
const leafletMap = shallowRef<L.Map>()


watch(geomLayerData, (newVal) => {
    if (newVal && newVal.length > 0) {
        var markers = L.markerClusterGroup();
        const markersList = newVal.map((geoData: GeomData) => L.marker([geoData.geom.coordinates[0], geoData.geom.coordinates[1]]))
        markers.addLayers(markersList);
        if (!leafletMap.value) {
            console.log("Map is not initiated, couldn't add markers");
            return;
        }
        leafletMap.value.addLayer(markers);
    }
})

onMounted(() => {
    initLeafletMap();
    L.Icon.Default.prototype.options.className = "mapMarker";
})

function initLeafletMap() {
    leafletMap.value = L.map('musicMap').setView([53, 12], 2);
    L.tileLayer('https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg', {
        minZoom: 2,
        maxZoom: 10,
        attribution: '&copy; <a href="https://stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://stamen.com/" target="_blank">Stamen Design</a> &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a>',
    }).addTo(leafletMap.value);
    createCountriesLayer();
}


async function loadCountries() {
    return await shp(`${FRONT_PUBLIC_URL}/geodata/ne_110m_admin_0_countries`);
}

async function createCountriesLayer() {
    if (countriesLayerBuffers.status.value === "error") {
        console.error(countriesLayerBuffers.error.value)
        return
    }
    else if (countriesLayerBuffers.status.value === "pending" || countriesLayerBuffers.status.value === "idle") {
        console.log("countries layers loading still pending");
        return
    }
    const res = countriesLayerBuffers.data.value;

    if (!res) {
        console.error("no result for countries layer");
        return
    }
    if (!leafletMap.value) {
        console.error("no map instanciated");
        return;
    }
    countriesLayer.value = L.geoJSON(res, {
        style: style.default,
        onEachFeature: onEachFeature
    }).addTo(leafletMap.value);
}

function onEachFeature(feature: any, layer: any) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: pickCountry
    })
}

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

function highlightFeature(e: any) {
    let layer = e.target;
    layer.setStyle(style.hilight);
}

function resetHighlight(e: any) {
    countriesLayer.value.resetStyle(e.target);
}

async function pickCountry(event: any) {
    if (!editionId.value) {
        return;
    }

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
    const centroid = turf.centerOfMass(pickedPolygon.toGeoJSON()); // pickedPolygon.getCenter() requires polygon to be loaded on the map
    const countryName = event.target.feature.properties["NAME"];
    const centroidLatLong = new L.LatLng(centroid.geometry.coordinates[0], centroid.geometry.coordinates[1]);
    if (!marker.value) {
        marker.value = L.marker(centroidLatLong, { title: countryName });// TODO try autoPanOnFocus : true, bubblingMouseEvents: true
        // lets customize default icon.

        marker.value.addTo(leafletMap.value)
        // .bindPopup(countryName)
        // .openPopup();
        marker.value.on({
            // hilight feature to disambiguate marker parenting
            mouseover: markerMouseOver,
            mouseout: markerMouseOut
        })
    } else {
        marker.value.title = countryName;
        marker.value.setLatLng(centroidLatLong);
    }
    marker.value.feature = event.target.feature;

    editorContext.value?.callback({ countryName: countryName, geom: centroid.geometry });
}

function markerMouseOver() {
    countriesLayer.value.eachLayer((layer: any) => {
        if (layer.feature === marker.value.feature) {
            layer.setStyle(style.hilight);
        }
    })
}

function markerMouseOut(e: any) {
    countriesLayer.value.eachLayer((layer: any) => {
        if (layer.feature === marker.value.feature) {
            layer.setStyle(style.default);
        }
    })
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