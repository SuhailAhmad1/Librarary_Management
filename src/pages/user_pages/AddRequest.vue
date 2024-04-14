<template>
    <the-header></the-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-dialog :show="isLoading" fixed title="Updating...">
        <base-spinner></base-spinner>
    </base-dialog>
    <base-card>
        <h2>Book Info</h2>
        <h3>Book Name : {{ item_name }}</h3>
        <h4>Author : {{ author }}</h4>
    </base-card>
    <base-card>
        <form @submit.prevent="submitForm">
            <div class="form-control">
                <label for="num_days">Number of days</label>
                <input type="number" id="num_days" v-model.number="no_of_days">
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="actions">
                <base-button>Request</base-button>
            </div>
        </form>
    </base-card>
</template>

<script>
import TheHeader from '../../components/layout/TheHeader.vue';

export default {
    components: {
        TheHeader
    },
    props: ["cat_id", "id"],
    data() {
        return {
            item_id: 0,
            item_name: '',
            author: '',
            no_of_days: null,
            formIsValid: true,
            error: null,
            isLoading: false
        }
    },
    methods: {
        closeError() {
            this.error = null;
        },
        async submitForm() {
            this.formIsValid = true;
            if (this.buy_quantity === 0 || this.notes === '' ) {
                console.log("error...")
                this.formIsValid = false;
                return;
            }
            try {
                this.isLoading = true
                await this.$store.dispatch('cart/addToRequest', {
                    product_id: this.item_id,
                    no_of_days: this.no_of_days
                })
            } catch (err) {
                this.isLoading = false
                this.error = err.message || "Failed to add to the Requests"
            }
            if (this.error == null) {
                this.isLoading = false
                this.$router.replace("/requests")
            }
        },
        get_item_info() {
            const all_cat = this.$store.getters['items/items'];
            const cat = all_cat.find(cat => cat.cat_id == this.cat_id)
            const item = cat.products.find(it => it.id == this.id);
            if (item) {
                this.item_id = this.id;
                this.item_name = item.itemName;
                this.author = item.author;
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
h2{
    text-align: center;
    font-size: 30px;
}
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
    justify-content: flex-end
}
</style>