<template>
    <div id="webviewer" ref="viewer"></div>
</template>

<script>
import webViewer from '@pdftron/webviewer'
import { ref, onMounted } from 'vue';

export default {
    name: 'WebViewer',
    props: { initialDoc: { type: String } },
    data() {
        return {
            isLoading: true
        }
    },
    setup(props) {
        const viewer = ref(null);
        onMounted(() => {
            setTimeout(() => {
                const path = "/webviewer";
                webViewer({ path, initialDoc: props.initialDoc, disabledElements: ['downloadButton', 'printButton', "saveAsButton"] }, viewer.value);
            }, 1000)
        })
        return { viewer }
    }
}
</script>

<style>
#webviewer {
    height: 89vh;
}
</style>