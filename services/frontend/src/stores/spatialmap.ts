import { defineStore } from "pinia";
import type { ArtistMapEditorContext, GeomData } from "~/commons/interfaces";

export const useSpatialMapStore = defineStore('spatialMap', () => {
    const editionId = ref<string>();
    const editorContext = ref<ArtistMapEditorContext>();

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

    function addLayerData(data: GeomData[]) {
        geomLayerData.value = data;
    }

    function updateLayerData(data: GeomData[]) {
        if (!geomLayerData.value) {
            geomLayerData.value = data;
            return;
        }
        const valuesToPush: GeomData[] = [];
        data.forEach((geomData: GeomData) => {
            //@ts-ignore
            const existingData = geomLayerData.value.find((g) => g.id === geomData.id);
            if (existingData) {
                existingData.geom = geomData.geom;
            }
            else {
                valuesToPush.push(geomData);
            }
        })
        if (valuesToPush.length > 0) {
            const newArray = geomLayerData.value.concat(valuesToPush)
            geomLayerData.value = newArray;
        }
    }

    return { editionId, editorContext, geomLayerData, openEditionForId, closeEditionId, addLayerData, updateLayerData };
});