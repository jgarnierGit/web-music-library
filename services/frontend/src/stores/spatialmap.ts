import { defineStore } from "pinia";
import { COUNTRY_FIELD_NAME } from "~/commons/constants";
import type { ArtistMapEditorContext, GeomData } from "~/commons/interfaces";
import * as turf from '@turf/turf';
import L from 'leaflet';

export const useSpatialMapStore = defineStore('spatialMap', () => {
    const editionId = ref<string>();
    const editorContext = ref<ArtistMapEditorContext>();
    const countriesLayer = ref<any>();
    const countriesFeatures = ref();
    const geomLayerData = ref<GeomData[]>()

    function openEditionForId(id: string, context: ArtistMapEditorContext) {
        editionId.value = id;
        editorContext.value = context;
    }

    function closeEditionId(id: string) {
        if (editionId.value !== id) {
            console.warn(`${id} wasn't in edition anyway`);
            return;
        }
        editionId.value = undefined;
    }

    function updateLayerData(data: GeomData[]) {
        if (!geomLayerData.value) {
            geomLayerData.value = data;
            return;
        }
        const valuesToPush: GeomData[] = [];
        data.forEach((geomData: GeomData) => {
            //@ts-ignore
            const existingDataId = geomLayerData.value.findIndex((g) => g.id === geomData.id);
            if (existingDataId !== -1) {
                // must remove and reinsert to trigger cluster updates
                geomLayerData.value?.splice(existingDataId, 1);
            }
            valuesToPush.push(geomData);
        })
        if (valuesToPush.length > 0) {
            const newArray = geomLayerData.value.concat(valuesToPush)
            geomLayerData.value = newArray;
        }
    }

    function setCountriesFeatures(countryFeatures: any) {
        countriesFeatures.value = countryFeatures;
    }

    function setCountriesLayer(countryLayer: L.GeoJSON) {
        countriesLayer.value = countryLayer;
    }

    function getGeomFromLabel(countryName: string) {
        let geom;
        countriesLayer.value.eachLayer((layer: any) => {
            if (countryName === layer.feature.properties[COUNTRY_FIELD_NAME]) {
                const pickedPolygon: L.Polygon<any> = L.polygon(layer.feature.geometry.coordinates);
                geom = turf.centerOfMass(pickedPolygon.toGeoJSON());
                geom = geom.geometry;
                return
            }
        });
        return geom;
    }

    return { editionId, editorContext, geomLayerData, countriesLayer, countriesFeatures, openEditionForId, closeEditionId, updateLayerData, getGeomFromLabel, setCountriesLayer, setCountriesFeatures };
});