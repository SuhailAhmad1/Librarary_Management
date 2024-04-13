<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <base-card>
            <header>
                <h2>Cart Items</h2>
            </header>
            <div v-if="isLoading">
                <base-spinner></base-spinner>
            </div>
            <h3 v-else-if="!get_cart_items.length">You haven't recieved any requests yet!</h3>
            <ul>
                <cart-item v-for="item in get_cart_items" :key="item.cart_id" :id="item.cart_id"
                    :itemName="item.product_name" :rate="item.rate" :quantity="item.quantity" :amount="item.amount"
                    :notes="item.notes"></cart-item>
            </ul>
            <div v-if="get_cart_items.length" class="actions">
                <h3>Grand Total : {{ total_amount }}</h3>
                <base-button link :to="buyItem">Buy All</base-button>
            </div>

        </base-card>
    </section>
</template>

<script>
import TheHeader from '../../../components/layout/TheHeader.vue';
import CartItem from "../../../components/items/CartItem.vue"
export default {
    components: {
        CartItem,
        TheHeader
    },
    data() {
        return {
            isLoading: false,
            error: null,
        };
    },
    methods: {
        closeError() {
            this.error = null;
        },
    },
    computed: {
        buyItem(){
            return "/place_order"
        },
        get_cart_items() {
            return this.$store.getters['cart/cart_items'];
        },
        total_amount() {
            const all_items = this.get_cart_items;
            const totalAmount = all_items.reduce((total, item) => total + item.amount, 0);
            return totalAmount
        }
    },
    async created() {
        try {
            await this.$store.dispatch('cart/setCartItems');
        } catch (err) {
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style scoped>
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
</style>