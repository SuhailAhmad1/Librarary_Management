<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h3 v-if="!get_request_items.length">No User Requests found</h3>
        <table v-else>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>No of Days</th>
                    <th>User</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(request, index) in get_request_items" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ request.book_name }}</td>
                    <td>{{ request.author }}</td>
                    <td>{{ request.days_requested }}</td>
                    <td>{{ request.user }}</td>
                    <td :class="status_color(request.status)">{{ request.status }}</td>
                    <td>
                        <button class="tooltip" :disabled="request.status !== 'Pending'"
                            @click="updateRequest(1, request.id)">
                            <svg class="tick" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="green"
                                width="24" height="24">
                                <path d="M0 0h24v24H0V0z" fill="none" />
                                <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" />
                            </svg>
                            <span class="tooltiptext">Approve</span>
                        </button>
                        <button class="tooltip" :disabled="request.status !== 'Pending'"
                            @click="updateRequest(-1, request.id)">
                            <svg class="cross" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="red"
                                width="24" height="24">
                                <path d="M0 0h24v24H0V0z" fill="none" />
                                <path
                                    d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z" />
                            </svg>
                            <span class="tooltiptext">Reject</span>
                        </button>
                    </td>
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
            error: null,
        };
    },
    methods: {
        async updateRequest(new_status, request_id) {
            try {
                await this.$store.dispatch('manager_items/updateRequestStatus', {
                    request_id: request_id,
                    status: new_status
                })
            } catch (err) {
                this.error = err.message || "Failed to load"
            }

            try {
                await this.$store.dispatch('manager_items/setUserRequestItems');
            } catch (err) {
                this.error = err.message || "Failed to load"
            }
        },
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
            return this.$store.getters['manager_items/userRequests'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('manager_items/setUserRequestItems');
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style scoped>
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 120px;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 0;
    position: absolute;
    z-index: 1;
    top: 150%;
    left: 50%;
    margin-left: -60px;
}

.tooltip .tooltiptext::after {
    content: "";
    position: absolute;
    bottom: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: transparent transparent black transparent;
}

.tooltip:hover .tooltiptext {
    visibility: visible;
}

button {
    border: none;
    margin-left: 3px;
    /* background-color: transparent; */
    cursor: pointer;
}
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

</style>