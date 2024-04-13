<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-dialog :show="isLoading" fixed title="Updating...">
        <base-spinner></base-spinner>
    </base-dialog>
    <base-card>
        <h3>Item Name : {{ item_name }}</h3>
        <h4>Rate : Rs. {{ item_rate }}</h4>
        <h5>Quantity Available : {{ item_quantity }}</h5>
    </base-card>
    <base-card>
        <form @submit.prevent="submitForm">
            <div class="form-control">
                <label for="quantity">Quantity</label>
                <input type="number" id="item_quantity" v-model.number="buy_quantity">
            </div>
            <div class="form-control">
                <label for="message">Additional Instructions</label>
                <textarea id="message" rows="5" v-model.trim="notes"></textarea>
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="actions">
                <h3>Total Amount : Rs. {{ total_amount }}</h3>
                <base-button>Add to Cart</base-button>
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
    props: ["cat_id", "id"],
    data() {
        return {
            item_id: 0,
            item_name: '',
            item_rate: 0,
            item_quantity: 0,
            buy_quantity: null,
            total_amount: 0,
            notes: '',
            formIsValid: true,
            error: null,
            isLoading: false
        }
    },
    watch: {
        buy_quantity() {
            this.total_amount = this.buy_quantity * this.item_rate;
        }
    },
    methods: {
        closeError() {
            this.error = null;
        },
        async submitForm() {
            this.formIsValid = true;
            if (this.buy_quantity === 0 || this.notes === '' || this.buy_quantity > this.item_quantity) {
                console.log("error...")
                this.formIsValid = false;
                return;
            }
            try {
                this.isLoading = true
                await this.$store.dispatch('cart/addToCart', {
                    product_id: this.item_id,
                    quantity: this.buy_quantity,
                    notes: this.notes,
                    amount: this.total_amount,
                    rate: this.item_rate
                })
            } catch (err) {
                this.isLoading = false
                this.error = err.message || "Failed to add to the Cart"
            }
            if (this.error == null) {
                this.isLoading = false
                this.$router.replace("/cart")
            }
        },
        get_item_info() {
            const all_cat = this.$store.getters['items/items'];
            const cat = all_cat.find(cat => cat.cat_id == this.cat_id)
            const item = cat.products.find(it => it.id == this.id);
            if (item) {
                this.item_id = this.id;
                this.item_name = item.itemName;
                this.item_rate = item.rate;
                this.item_quantity = item.quantity;
                return true;
            }
            return false
        }
    },
    async created() {
        await this.$store.dispatch('items/loadItems', { forceRefresh: true });
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

.actions {
    text-align: center;
    display: flex;
    justify-content: space-between;
}
</style>