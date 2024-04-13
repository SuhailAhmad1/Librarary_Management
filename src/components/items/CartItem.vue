<template>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <li>
        <h3>{{ itemName }}</h3>
        <h4>Rate : Rs. {{ rate }}</h4>
        <h5>Quantity : {{ quantity }}</h5>
        <h5>Additional note : {{ notes }}</h5>
        <div class="footer">
            <h4>Amount : {{ amount }}</h4>
            <div class="actions">
                <base-button link :to="editItem">Edit</base-button>
                <base-button mode="red" @click="deleteItem()">Delete</base-button>
            </div>
        </div>
    </li>
</template>

<script>
export default {
    props: ["id", "itemName", "rate", "quantity", "category", "amount", "notes"],
    data() {
        return {
            error: null
        }
    },
    methods: {
        closeError() {
            this.error = null;
        },
        async deleteItem() {
            try {
                await this.$store.dispatch('cart/deleteItem', {
                    id: this.id
                })
            }
            catch (err) {
                this.error = err.message || "Failed to delete Cart Item"
            }
        }
    },
    computed: {
        editItem() {
            return "/cart/" + this.id + "/edit";
        }
    }
}
</script>

<style scoped>
li {
    margin: 1rem 0;
    border: 1px solid #424242;
    border-radius: 12px;
    padding: 1rem;
    background-color: rgba(25, 29, 29, 0.7);
}

h3 {
    font-size: 1.8rem;
}

h3,
h4 {
    margin: 0.5rem 0;
}

div {
    margin: 0.5rem 0;
}

.footer {
    display: flex;
    justify-content: space-between;
}

.actions {
    display: flex;
    justify-content: flex-end;
}
</style>