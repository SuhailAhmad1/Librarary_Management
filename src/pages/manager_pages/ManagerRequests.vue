<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h3>My Requests</h3>
        <table>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Action</th>
                    <th>Category</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(request, index) in get_all_requests['category_requests']" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td :class="type_color(request.type)">{{ request.type }}</td>
                    <td>{{ request.category ? request.category : "----" }}</td>
                    <td :class="status_color(request.status)">{{ request.status }}</td>
                </tr>
            </tbody>
        </table>
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
        },
        status_color(status) {
            if (status == "Pending")
                return "placed_status"
            else if (status == "Approved")
                return "delivered_status"
            else if (status == "Rejected")
                return "cancel_status"
        },
        type_color(type) {
            if (type == "CREATE")
                return "create_type"
            else if (type == "EDIT")
                return "edit_type"
            else if (type == "DELETE")
                return "delete_type"
        }
    },
    computed: {
        get_all_requests() {
            return this.$store.getters['manager_items/managerRequests'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('manager_items/setRequestItems');
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
.create_type {
    color: rgb(51, 238, 76);
    font-weight: bold;
}
.edit_type {
    color: rgb(107, 73, 228);
    font-weight: bold;
}
.delete_type {
    color: rgb(240, 53, 53);
    font-weight: bold;
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
    margin: 30px auto;
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