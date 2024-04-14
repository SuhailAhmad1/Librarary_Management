<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-card>
        <base-dialog :show="isLoading" fixed title="Updating...">
            <base-spinner></base-spinner>
        </base-dialog>
        <h3>Edit Book Details</h3>
        <form @submit.prevent="submitForm">
            <div class="form-control">
                <label for="item_name">Book Name</label>
                <input type="text" id="item_name" v-model="item_name">
            </div>
            <div class="form-control">
                <label for="item_rate">Author</label>
                <input type="text" id="item_quantity" v-model="item_author">
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="actions">
                <base-button>Update</base-button>
            </div>
        </form>
    </base-card>
</template>

<script>
import TheManagerHeader from '../../components/layout/TheManagerHeader.vue'
export default {
    components: {
        TheManagerHeader
    },
    props: ["cat_id", "id"],
    data() {
        return {
            isLoading: false,
            item_id: null,
            item_name: null,
            item_author: null,
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
            if (this.item_quantity === 0 || this.item_name === '' || this.item_rate <= 0) {
                console.log("error...")
                this.formIsValid = false;
                return;
            }
            try {
                this.isLoading = true;
                await this.$store.dispatch('manager_items/editItem', {
                    id: this.item_id,
                    itemName: this.item_name,
                    author: this.item_author,
                })
            } catch (err) {
                this.isLoading = false;
                this.error = err.message || "Failed to edit";
            }
            this.isLoading = false
            if (this.error == null) {
                this.$router.replace("/home/manager")
            }
        },
        get_item_info() {
            const all_cat = this.$store.getters['manager_items/managerItems'];
            const cat = all_cat.find(cat => cat.cat_id == this.cat_id)
            const item = cat.products.find(it => it.id == this.id);
            if (item) {
                this.item_id = this.id;
                this.item_name = item.itemName;
                this.item_author = item.author;
                return true;
            }
            return false
        }
    },
    async created() {
        await this.$store.dispatch('manager_items/setAPIdata');
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
    display: flex;
    justify-content: flex-end;
}

h3 {
    text-align: center;
    font-size: 1.5rem;
    color: rgb(255, 255, 255);
}
</style>