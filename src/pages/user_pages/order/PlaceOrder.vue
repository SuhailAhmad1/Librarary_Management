<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-card>
        <base-dialog :show="isLoading" fixed title="Placing order...">
            <base-spinner></base-spinner>
        </base-dialog>
        <h3>Add Order Details</h3>
        <form @submit.prevent="submitForm">
            <div class="form-control">
                <label for="name">Full Name</label>
                <input type="text" id="name" v-model="full_name">
            </div>
            <div class="form-control">
                <label for="phone_number">Phone Number</label>
                <input type="text" id="phone_number" v-model="phone_number">
            </div>
            <div class="form-control">
                <label for="address">Order Address</label>
                <input type="text" id="address" v-model="order_address">
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="actions">
                <base-button>Place Order</base-button>
            </div>
        </form>
    </base-card>
</template>

<script>
import TheHeader from "../../../components/layout/TheHeader.vue"

export default {
    components: {
        TheHeader
    },
    props: ["id"],
    data() {
        return {
            isLoading: false,
            full_name: "",
            order_address: "",
            phone_number: "",
            formIsValid: true,
            error: null
        }
    },
    methods: {
        closeError() {
            this.error = null;
        },
        async submitForm() {
            this.formIsValid = true;
            if (this.full_name.length === 0 || this.order_address.length < 5 || this.phone_number.length != 10) {
                this.formIsValid = false;
                return;
            }
            this.isLoading = true;
            try {
                await this.$store.dispatch('user_orders/placeOrder', {
                    full_name: this.full_name,
                    address: this.order_address,
                    phone_number: this.phone_number
                })
            } catch (err) {
                this.isLoading = false;
                this.error = err.message || "Failed to edit";
            }
            this.isLoading = false
            if (this.error == null) {
                this.$router.replace("/orders")
            }
        }
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
    display: flex;
    justify-content: flex-end;
}

h3 {
    text-align: center;
    font-size: 1.5rem;
    color: rgb(255, 255, 255);
}
</style>