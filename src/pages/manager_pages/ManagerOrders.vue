<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <h3 v-if="!get_order_items.length">No orders found yet!</h3>
        <table v-else>
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Product</th>
                    <th>Quantity</th>
                    <th>Amount</th>
                    <th>Full Name</th>
                    <th>Contact</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(order, index) in get_order_items" :key="order.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ order.product_name }}</td>
                    <td>{{ order.quantity }}</td>
                    <td>Rs. {{ order.amount }}</td>
                    <td>{{ order.name }}</td>
                    <td>{{ order.phone_number }}</td>
                    <td>{{ order.address }}</td>
                    <td :class="status_color(order.status)">{{ order.status }}</td>
                    <td class="actions">
                        <base-button @click="toggleDropdown(index)">Edit Status</base-button>
                        <ul v-if="isDropdownOpen(index)">
                            <li @click="updateStatus(order.id, 'Shipped')">Shipped</li>
                            <li @click="updateStatus(order.id, 'Delivered')">Delivered</li>
                            <li @click="updateStatus(order.id, 'Cancel')">Cancel</li>
                        </ul>
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
            openDropdowns: []
        };
    },
    methods: {
        async updateStatus(order_id, new_status) {
            try {
                await this.$store.dispatch('manager_items/updateOrderStatus', {
                    order_id: order_id,
                    status: new_status
                })
            } catch (err) {
                this.error = err.message || "Failed to load"
            }

            try {
                await this.$store.dispatch('manager_items/setOrderItems');
            } catch (err) {
                this.error = err.message || "Failed to load"
            }
            this.openDropdowns = []
        },
        closeError() {
            this.error = null;
        },
        toggleDropdown(index) {
            if (this.openDropdowns.includes(index)) {
                this.openDropdowns = this.openDropdowns.filter(i => i !== index); // Close dropdown if already open
            } else {
                this.openDropdowns = []
                this.openDropdowns.push(index); // Open dropdown
            }
        },
        isDropdownOpen(index) {
            return this.openDropdowns.includes(index); // Check if dropdown is open for the given index
        },
        status_color(status) {
            if (status == "Placed")
                return "placed_status"
            else if (status == "Shipped")
                return "shipped_status"
            else if (status == "Delivered")
                return "delivered_status"
            else if (status == "Cancel")
                return "cancel_status"
        }
    },
    computed: {
        get_order_items() {
            return this.$store.getters['manager_items/managerOrders'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('manager_items/setOrderItems');
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