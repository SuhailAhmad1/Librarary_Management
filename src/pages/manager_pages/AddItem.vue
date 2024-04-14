<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <base-card>
        <base-dialog :show="isLoading" fixed title="Adding...">
            <base-spinner></base-spinner>
        </base-dialog>
        <h3>Add Book</h3>
        <form @submit.prevent="submitForm">
            <div class="form-control">
                <label for="item_name">Title</label>
                <input type="text" id="item_name" v-model="item_name">
            </div>
            <div class="form-control">
                <label for="item_author">Author </label>
                <input type="text" id="item_author" v-model="item_author">
            </div>
            <div class="form-control">
                <label for="item_quantity">Upload Book</label>
                <input type="file" @change="handleFileUpload">
            </div>
            <p class="errors" v-if="!formIsValid">Please enter valid data.</p>
            <div class="actions">
                <base-button>Add Item</base-button>
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
            item_name: "",
            item_author: "",
            selectedFile: null,
            formIsValid: true,
            error: null
        }
    },
    methods: {
        handleFileUpload(event) {
            const files = event.target.files;
            if (files.length > 1) {
                // More than one file selected
                alert('Please select only one file.');
                event.target.value = ''; // Reset the file input
                return;
            }
            const file = files[0];
            if (!file) {
                // No file selected
                return;
            }
            // Check if the selected file is a PDF
            if (file.type === 'application/pdf') {
                this.selectedFile = file;
            } else {
                alert('Please select a PDF file.');
                event.target.value = ''; // Reset the file input
            }

        },
        closeError() {
            this.error = null;
        },
        async submitForm() {
            console.log(this.selectedFile)
            this.formIsValid = true;
            if (this.item_author === 0 || this.item_name === '' || this.selectedFile === null) {
                console.log("error...")
                this.formIsValid = false;
                return;
            }
            this.isLoading = true;
            try {
                await this.$store.dispatch('manager_items/addItem', {
                    itemName: this.item_name,
                    author: this.item_author,
                    file: this.selectedFile,
                    category_id: this.id
                })
            } catch (err) {
                this.isLoading = false;
                this.error = err.message || "Failed to edit";
            }
            this.isLoading = false
            if (this.error == null) {
                this.$router.replace("/home/manager")
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