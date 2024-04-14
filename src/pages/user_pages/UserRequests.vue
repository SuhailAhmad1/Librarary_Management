<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h3 v-if="!get_request_items.length">No requests found</h3>
        <table v-else>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>No of Days</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(request, index) in get_request_items" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ request.book_name }}</td>
                    <td>{{ request.author }}</td>
                    <td>{{ request.days_requested }}</td>
                    <td :class="status_color(request.status)">{{ request.status }}</td> 
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>
import TheHeader from '../../components/layout/TheHeader.vue'
export default {
    components: {
        TheHeader
    },
    data() {
        return {
            isLoading: false,
            error: null,
            openDropdowns: []
        };
    },
    methods: {
        closeError() {
            this.error = null;
        },
        status_color(status) {
            if (status == "Pending")
                return "placed_status"
            else if (status == "Approved")
                return "delivered_status"
            else if (status == "Rejected")
                return "cancel_status"
        }
    },
    computed: {
        get_request_items() {
            return this.$store.getters['cart/request_items'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('cart/setRequestItems');
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style scoped>
section {
    padding: 2rem;
    margin: 3rem;
    background-color: rgb(23, 16, 37);
    border-radius: 1rem;
}

.placed_status {
    background-color: rgb(34, 12, 114);
}

.shipped_status {
    background-color: rgb(0, 92, 121);
}

.delivered_status {
    background-color: rgb(0, 110, 15);
}

.cancel_status {
    background-color: rgb(141, 0, 0);
}

header {
    text-align: center;
}

ul {
    list-style: none;
    margin: 2rem auto;
    padding: 0;
    max-width: 30rem;
}

h3,
h5 {
    text-align: center;
}

.actions {
    margin: auto;
}

table {
    width: 95%;
    margin: 20px auto;
    text-align: center;
    border-collapse: collapse;
}

th {
    padding: 1.0rem;
    font-size: 1rem;
    font-weight: bold;
    border: 0.2px solid rgb(79, 100, 90);
    background-color: #00503c;
}

td {
    padding: 0.8rem;
    font-size: 0.7rem;
    border: 1px solid #384747;
}

.dropdown {
    position: relative;
    display: inline-block;
}

ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
    border: 1px solid #ccc;
    background-color: #413838;
    position: absolute;
    left: 80%;
    z-index: 1;
}

li {
    padding: 8px;
    cursor: pointer;
}

li:hover {
    background-color: #161515;
}
</style>