<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <WebViewer :initialDoc="get_pdf_url"></WebViewer>
</template>

<script>
import WebViewer from '../../components/items/WebViewer.vue'
import TheManagerHeader from '../../components/layout/TheManagerHeader.vue'
export default {
    components: {
        WebViewer,
        TheManagerHeader
    },
    props: ["id"],
    data() {
        return {
            isLoading: false,
            error: null
        }
    },
    methods: {
        closeError() {
            this.error = null;
        },
    },
    computed: {
        get_pdf_url() {
            return this.$store.getters['manager_items/managerBook'];
        }
    },
    async created() {
        console.log("Creating...")
        try {
            await this.$store.dispatch('manager_items/setBookPdf', {
                id: this.id
            });
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
}
</script>