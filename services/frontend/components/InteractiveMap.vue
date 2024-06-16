<template>

    <v-row>
        <v-col>
            <v-container id="mapInterface">
                <v-btn @click="switchView()">switch view</v-btn>
            </v-container>
            <v-sheet height="90vh" rounded="lg">
                <div ref="viewerDiv" id="viewerDiv" @click="pickCountry($event)">
                </div>
            </v-sheet>
        </v-col>
    </v-row>
</template>
<script setup lang="ts">
// @ts-ignore 
import * as itowns from 'itowns';

const viewerDiv = ref();
const is3D = ref(false);
const countriesLayerBuffers = await useAsyncData('countries', () => loadCountries());
const countriesLayer = ref();
const renderer = ref();
const mapStore = useSpatialMapStore();
const { editionId, editorContext } = storeToRefs(mapStore);


var view: any;

const styles = {
    default: {
        fill: { color: 'white', opacity: 0 },
        stroke: { color: 'black' }
    }
}

onMounted(() => {
    create2DMap();
    renderer.value = view.renderer;
});

function pickCountry(event: MouseEvent) {
    if (!view || !editionId.value) { return }
    // TODO overwrite cursor grab changing to default cursor. (check in itowns)
    const pickedData = view.pickFeaturesAt(event, 3, countriesLayer.value);
    const value = pickedData.countries[0].geometry.properties["NAME"];
    console.log(pickedData.countries[0].geometry.properties)
    editorContext.value?.callback(value);

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
    const geojson = await itowns.ShapefileParser.parse({
        shp: res[0],
        dbf: res[1],
        shx: res[2],
        prj: res[3],
    }, {
        in: {
            crs: 'EPSG:4326',
        },
        out: {
            crs: view.tileLayer.extent.crs,
        }
    });
    console.log(JSON.stringify(geojson))
    //@ts-ignore no features properties
    const countriesSource = new itowns.FileSource({ features: geojson });
    const layer = new itowns.ColorLayer('countries', {
        source: countriesSource, style: styles.default,
    });
    return layer;
}

async function create3DMap() {
    // Define camera initial position
    const placement = {
        coord: new itowns.Coordinates('EPSG:4326', 2.351323, 48.856712),
        range: 25000000,
    }

    // Create a GlobeView
    view = new itowns.GlobeView(viewerDiv.value, placement, { renderer: renderer.value || {} });
    const openSMLayer = getOpenSMLayer();

    view.addLayer(openSMLayer);
    countriesLayer.value = await createCountriesLayer()
    view.addLayer(countriesLayer.value);

    // ADD A SEARCH BAR :

    // You can find more precise explanation on searchbar options in the doc
    // (http://www.itowns-project.org/itowns/docs/#api/Widgets/Searchbar) and in the searchbar example
    // (https://www.itowns-project.org/itowns/examples/#widgets_searchbar)

    // Define options for geocoding service that should be used by the searchbar.
    const geocodingOptions = {
        url: new URL(
            'https://data.geopf.fr/geocodage/completion?' +
            'text=&type=StreetAddress,PositionOfInterest',
        ),
        parser: (response: any) => {
            const map = new Map();
            response.results.forEach((location: any) => {
                map.set(location.fulltext, new itowns.Coordinates('EPSG:4326', location.x, location.y));
            });
            return map;
        },
        onSelected: (coordinates: any) => {
            view.controls?.lookAtCoordinate({ coord: coordinates, range: 20000, tilt: 45, heading: 0 });
        },
    }
    /** 
        // Create the searchbar
        const searchbar = new itowns_widgets.Searchbar(view, geocodingOptions, {
            maxSuggestionNumber: 15,
            placeholder: 'Search a location in France',
            position: 'top-right',
        });
    */
    is3D.value = true;
}

async function loadCountries() {
    return await Promise.all([
        itowns.Fetcher.arrayBuffer('./geodata/ne_110m_admin_0_countries.shp'),
        itowns.Fetcher.arrayBuffer('./geodata/ne_110m_admin_0_countries.dbf'),
        itowns.Fetcher.arrayBuffer('./geodata/ne_110m_admin_0_countries.shx'),
        itowns.Fetcher.text('./geodata/ne_110m_admin_0_countries.prj'),
    ]);

}

function getOpenSMLayer() {
    // Add a TMS imagery source
    var opensmSource = new itowns.TMSSource({
        isInverted: true,
        // eslint-disable-next-line no-template-curly-in-string
        url: 'https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/${z}/${x}/${y}.jpg',
        networkOptions: { crossOrigin: 'anonymous' },
        crs: 'EPSG:3857',
        attribution: {
            name: 'OpenStreetMap',
            url: 'http://www.openstreetmap.org/',
        },
    });

    // Add a TMS imagery layer
    var opensmLayer = new itowns.ColorLayer('OPENSM', {
        updateStrategy: {
            type: itowns.STRATEGY_DICHOTOMY,
        },
        source: opensmSource,
    });
    return opensmLayer;
}

async function create2DMap() {
    var extent = new itowns.Extent(
        'EPSG:3857',
        -20026376.39, 20026376.39,
        -20048966.10, 20048966.10);

    view = new itowns.PlanarView(viewerDiv.value, extent, {
        disableSkirt: true, maxSubdivisionLevel: 10,
        camera: { type: itowns.CAMERA_TYPE.ORTHOGRAPHIC },
        placement: new itowns.Extent('EPSG:3857', -20000000, 20000000, -8000000, 20000000),
        controls: {
            // Faster zoom in/out speed
            zoomFactor: 3,
            // prevent from zooming in too much
            maxResolution: 0.005  // a pixel shall not represent a metric size smaller than 5 mm
        },
        renderer: renderer.value || {}
    });

    const opensmLayer = getOpenSMLayer();

    view.addLayer(opensmLayer);
    countriesLayer.value = await createCountriesLayer()
    view.addLayer(countriesLayer.value);

    // Request redraw
    view.notifyChange();
    is3D.value = false;
}


function switchView() {
    if (is3D.value) {
        view.dispose();
        create2DMap();
    }
    else {
        view.dispose();
        create3DMap();
    }
}
</script>

<style>
#mapInterface {
    position: absolute;
    z-index: 1;
}

#viewerDiv {
    width: 100%;
    height: 100%;
    opacity: 1 !important;
    background: white;
    z-index: 0;

    >div {
        height: auto !important;
    }
}
</style>