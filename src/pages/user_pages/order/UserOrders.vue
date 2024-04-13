<template>
    <the-header></the-header>
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
                    <th>Amount</th>
                    <th>Address</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(order, index) in get_order_items" :key="order.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ order.product_name }}</td>
                    <td>Rs. {{ order.amount }}</td>
                    <td>{{ order.address }}</td>
                    <td :class="status_color(order.status)">{{ order.status }}</td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>
import TheHeader from '../../../components/layout/TheHeader.vue';
export default {
    components: {
        TheHeader
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
        status_color(status){
            if(status == "Placed")
                return "placed_status"
            else if(status == "Shipped")
                return "shipped_status"
            else if(status == "Delivered")
                return "delivered_status"
            else if(status == "Cancel")
                return "cancel_status"
        }
    },
    computed: {
        get_order_items() {
            return this.$store.getters['user_orders/orderItems'];
        }
    },
    async created() {
        try {
            await this.$store.dispatch('user_orders/setOrderItems');
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style scoped>
section{
    padding: 2rem;
    margin: 5rem;
    background-color: rgb(23, 16, 37);
    border-radius: 1rem;
}
.placed_status{
    background-color: rgb(34, 12, 114);
}
.shipped_status{
    background-color: rgb(0, 92, 121);
}
.delivered_status{
    background-color: rgb(0, 110, 15);
}
.cancel_status{
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
    display: flex;
    justify-content: space-between;
}

table {
    width: 90%;
    margin: 20px auto;
    text-align: center;
    border-collapse: collapse;
}

th {
    padding: 1.5rem;
    font-size: large;
    border: 0.2px solid black;
}

td {
    padding: 1.5rem;
    border: 1px solid #1f2e2e;
}

th {
    background-color: #00503c;
    font-weight: bold;
}
</style>