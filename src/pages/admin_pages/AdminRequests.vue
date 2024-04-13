<template>
    <the-admin-header></the-admin-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h3>All Manager Requests</h3>
        <table>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Action</th>
                    <th>Data</th>
                    <th>Category</th>
                    <th>Manager</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(request, index) in get_all_requests['category_requests']" :key="request.id">
                    <td>{{ index + 1 }}</td>
                    <td :class="type_color(request.type)">{{ request.type }}</td>
                    <td>{{ request.request_data ? request.request_data : "----" }}</td>
                    <td>{{ request.category ? request.category : "----" }}</td>
                    <td>{{ request.manager }}</td>
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
import TheAdminHeader from '../../components/layout/TheAdminHeader.vue'
export default {
    components: {
        TheAdminHeader
    },
    data() {
        return {
            isLoading: false,
            error: null,
            showHoverText: false
        };
    },
    methods: {
        async updateRequest(status, request_id) {
            console.log("hjhkj")
            try {
                await this.$store.dispatch('admin_items/updateRequest', {
                    status: status,
                    request_id: request_id
                });
            } catch (err) {
                this.error = err.message || "Failed to update"
            }

            try {
                await this.$store.dispatch('admin_items/setRequestItems');
            } catch (err) {
                this.error = err.message || "Failed to load"
            }
        },

        showText() {
            this.showHoverText = true;
        },
        hideText() {
            this.showHoverText = false;
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
            return this.$store.getters['admin_items/adminRequests'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('admin_items/setRequestItems');
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
    background-color: rgb(11, 126, 26);
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



table {
    width: 95%;
    margin: 30px auto;
    text-align: center;
    border-collapse: collapse;
}

th {
    padding: 0.7rem;
    font-size: 1rem;
    font-weight: bold;
    border: 0.2px solid rgb(79, 100, 90);
    background-color: #00503c;
}

td {
    max-width: 150px;
    padding: 0.7rem;
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