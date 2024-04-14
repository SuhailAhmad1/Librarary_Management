<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <WebViewer :initialDoc="get_pdf_url"></WebViewer>
</template>

<script>
import WebViewer from '../../components/items/WebViewer.vue'
import TheHeader from '../../components/layout/TheHeader.vue'
export default {
    components: {
        WebViewer,
        TheHeader
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
            return this.$store.getters['cart/userBook'];
        }
    },
    async created() {
        console.log("Creating...")
        try {
            await this.$store.dispatch('cart/setBookPdf', {
                id: this.id
            });
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
}
</script>