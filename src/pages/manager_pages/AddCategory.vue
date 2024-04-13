<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-card>
        <base-dialog :show="isLoading" fixed title="Adding...">
            <base-spinner></base-spinner>
        </base-dialog>
        <h3>Add Category</h3>
        <form @submit.prevent="submitForm">
            <div class="form-control">
                <label for="item_name">Category Name</label>
                <input type="text" id="item_name" v-model="cat_name">
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="actions">
                <base-button>Add Category</base-button>
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
    props: ["id"],
    data() {
        return {
            isLoading: false,
            cat_name: null,
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
            if (this.cat_name.length === 0) {
                console.log("error...")
                this.formIsValid = false;
                return;
            }
            this.isLoading = true;
            try {
                await this.$store.dispatch('manager_items/addCategory', {
                    category: this.cat_name
                })
            } catch (err) {
                this.isLoading = false;
                this.error = err.message || "Failed to edit";
            }
            this.isLoading = false
            if (this.error == null) {
                this.$router.replace("/manager/requests")
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