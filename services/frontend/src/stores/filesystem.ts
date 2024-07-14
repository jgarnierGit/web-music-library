import { LIBRARY_VIEWS } from "~/commons/constants";

export const useFilesystemStore = defineStore('filesystem', () => {
    const refreshJobId = ref();
    const refreshingCurrentState = ref();
    const activeNavigatorView = ref({ target: LIBRARY_VIEWS[0] })
    const isCard = ref(true);

    function setRefreshJobId(jobId: string) {
        refreshJobId.value = jobId;
    }

    function clearRefreshJobId() {
        refreshJobId.value = undefined;
    }

    function updateCurrentState(value: number) {
        refreshingCurrentState.value = value;
    }
    function switchIsCard() {
        isCard.value = !isCard.value;
    }
    return { refreshJobId, refreshingCurrentState, activeNavigatorView, isCard, clearRefreshJobId, setRefreshJobId, updateCurrentState, switchIsCard };
});