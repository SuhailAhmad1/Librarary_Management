<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h3 v-if="!get_image_url.length">No statistics found yet!</h3>
        <img :src="get_image_url" alt="img failed" />
    </section>
</template>

<script>
import TheManagerHeader from '../../components/layout/TheManagerHeader.vue'
export default {
    components: {
        TheManagerHeader
    },
    data() {
        return {
            isLoading: false,
            error: null
        };
    },
    methods: {
        closeError() {
            this.error = null;
        }
    },
    computed: {
        get_image_url() {
            return this.$store.getters['manager_items/managerGraph'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('manager_items/setManagerGraph');
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style scoped>
section {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* Horizontally center the image */
    justify-content: center;
    /* Vertically center the image */
    padding-top: 5em;
    padding-bottom: 5em;
    margin: 3em;
    background-color: rgb(23, 16, 37);
    border-radius: 1em;
}

header {
    text-align: center;
}

img {
    margin: auto;
    border-radius: 1em;
    width: 60%;
    height: 60%;
}

h3,
h5 {
    text-align: center;
}

.actions {
    margin: auto;
}
</style>