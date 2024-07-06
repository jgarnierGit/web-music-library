export const useFilesystemStore = defineStore('filesystem', () => {
    const refreshJobId = ref();
    const refreshingCurrentState = ref()

    function setRefreshJobId(jobId: string) {
        refreshJobId.value = jobId;
    }

    function clearRefreshJobId() {
        refreshJobId.value = undefined;
    }

    function updateCurrentState(value: number) {
        refreshingCurrentState.value = value;
    }
    return { refreshJobId, refreshingCurrentState, clearRefreshJobId, setRefreshJobId, updateCurrentState };
});