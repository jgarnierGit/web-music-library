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

    function addLayer(data: GeomData[]) {
        geomLayerData.value = data;
    }


    return { editionId, editorContext, geomLayerData, openEditionForId, closeEditionId, addLayer };
});