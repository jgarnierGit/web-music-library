import { defineStore } from "pinia";

export const useProjectMStore = defineStore('projectM', () => {
    const isVisible = ref(false);
    const isFocused = ref(false);

    function toggleMilkdrop() {
        isVisible.value = !isVisible.value;
        if (!isVisible.value) {
            isFocused.value = false;
        }
    }

    function toggleFocusMode() {
        isFocused.value = !isFocused.value;
    }


    return { isVisible, isFocused, toggleMilkdrop, toggleFocusMode };
});