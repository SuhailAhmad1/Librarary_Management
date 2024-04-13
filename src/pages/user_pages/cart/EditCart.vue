<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-dialog :show="isLoading" fixed title="Updating...">
        <base-spinner></base-spinner>
    </base-dialog>
    <base-card>
        <h3>Edit Cart Item</h3>
        <form @submit.prevent="submitForm">
            <p>Item Name : {{ item_name }}</p>
            <p>Rate : Rs. {{ item_rate }}</p>
            <p>Available Quantity : {{ item_available_quanitity }}</p>
            <div class="form-control">
                <label for="item_quantity">Buy Quanitity</label>
                <input type="number" id="item_quantity" v-model.number="item_quantity">
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="footer">
                <h4>Amount : Rs. {{ calulate_amount }}</h4>
                <div class="actions">
                    <base-button>Update</base-button>
                </div>
            </div>
        </form>
    </base-card>
</template>

<script>
import TheHeader from '../../../components/layout/TheHeader.vue';

export default {
    components: {
        TheHeader
    },
    props: ["id"],
    data() {
        return {
            isLoading: false,
            item_id: null,
            item_name: null,
            item_rate: null,
            item_quantity: null,
            formIsValid: true,
            error: null,
            item_available_quanitity: null
        }
    },
    computed: {
        calulate_amount() {
            return this.item_rate * this.item_quantity;
        }
    },
    methods: {
        closeError() {
            this.error = null;
        },
        async submitForm() {
            this.formIsValid = true;
            if (this.item_quantity <= 0 || this.item_quantity > this.item_available_quanitity) {
                console.log("error...")
                this.formIsValid = false;
                return;
            }
            this.isLoading = true;
            try {
                await this.$store.dispatch('cart/editCartItem', {
                    cart_id: this.item_id,
                    quantity: this.item_quantity,
                    amount: this.calulate_amount,
                })
            } catch (err) {
                this.isLoading = false;
                this.error = err || 'Failed to edit, try again later!';
            }
            this.isLoading = false;
            if (this.error == null) {
                this.$router.replace("/cart")
            }
        },
        get_item_info() {
            const items = this.$store.getters['cart/cart_items'];
            console.log(items)
            const item = items.find(it => it.cart_id == this.id);
            if (item) {
                this.item_id = item.cart_id;
                this.item_name = item.product_name;
                this.item_rate = item.rate;
                this.item_quantity = item.quantity;
                this.item_available_quanitity = item.quantity_available;
                return true;
            }
            return false
        }
    },
    async created() {
        await this.$store.dispatch('cart/setCartItems');
        this.get_item_info();
    }
}
</script>

<style scoped>
form {
    margin: 1rem;
    border: 1px solid #ccc;
    border-radius: 12px;
    padding: 1rem;
}

.form-control {
    margin: 0.5rem 0;
}

label {
    font-weight: bold;
    margin-bottom: 0.5rem;
    display: block;
}

input,
textarea {
    display: block;
    width: 100%;
    font: inherit;
    border: 1px solid #ccc;
    padding: 0.15rem;
}

input:focus,
textarea:focus {
    border-color: #3d008d;
    background-color: #faf6ff;
    outline: none;
}

.errors {
    font-weight: bold;
    color: red;
}

.footer {
    display: flex;
    justify-content: space-between;
}

.actions {
    display: flex;
    justify-content: flex-end;
}

h3 {
    text-align: center;
    font-size: 1.5rem;
    color: rgb(255, 255, 255);
}
</style>