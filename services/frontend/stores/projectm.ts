import { defineStore } from "pinia";

export const useProjectMStore = defineStore('projectM', () => {
    const isVisible = ref(false);

    function toggleMilkdrop() {
        isVisible.value = !isVisible.value;
    }


    return { isVisible, toggleMilkdrop };
});