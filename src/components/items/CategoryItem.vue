<template>
    <base-dialog :show="!!error" title="Error occured" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <li>
        <div id="cat_header">
            <h3>{{ cat_name }}</h3>
            <div>
                <base-badge v-for="cat in category" :key="cat" :type="cat" :title="cat"></base-badge>
            </div>
            <div class="actions">
                <base-button mode="outline" link :to="addItem">+ Add Product</base-button>
                <base-button link :to="editItem">Edit</base-button>
                <base-button mode="red" @click="deleteItem()">Delete</base-button>
            </div>
        </div>
        <div class="scroll-container" v-if="!!products.length">
            <button class="scroll-button" @click="scrollLeft">&lt;</button>
            <div class="scroll-wrapper" ref="scrollWrapper">
                <div class="scroll-content">
                    <manager-item v-for="item in products" :key="item.id" :id="item.id" :itemName="item.itemName"
                        :rate="item.rate" :quantity="item.quantity" :cat_id="id" class="item"></manager-item>
                </div>
            </div>
            <button class="scroll-button" @click="scrollRight">&gt;</button>
        </div>
        <p v-else>No product created. Please create one</p>
    </li>
</template>

<script>
import ManagerItem from "./ManagerItem.vue"

export default {
    components: {
        ManagerItem
    },
    props: ["id", "cat_name", "products"],
    data() {
        return {
            error: null,
            scrollStep: 200
        }
    },
    methods: {
        scrollLeft() {
            this.$refs.scrollWrapper.scrollLeft -= this.scrollStep;
        },
        scrollRight() {
            this.$refs.scrollWrapper.scrollLeft += this.scrollStep;
        },
        closeError() {
            this.error = null;
        },
        async deleteItem() {
            try {
                await this.$store.dispatch('manager_items/deleteCategory', {
                    id: this.id
                })
                this.$router.replace("/manager/requests")
            } catch (err) {
                this.error = err.message || "Failed to delete"
            }
        }
    },
    computed: {
        fullName() {
            return this.firstName + " " + this.lastName;
        },
        editItem() {
            return "/manager/" + this.id + "/edit_category";
        },
        addItem() {
            return "/manager/"+ this.id +"/addItem";
        }
    }
}
</script>

<style scoped>
p{
    text-align: center;
}
li {
    margin: 1rem 0;
    border: 1px solid #424242;
    border-radius: 12px;
    padding: 1rem;
    background-color: rgba(25, 29, 29, 0.7);
    list-style: none;
    margin: 10px;
}

h3 {
    font-size: 1.8rem;
    margin-left: 10px;
}
h3,
h4 {
    margin: 0.5rem 0;
}

div {
    margin: 0.5rem 0;
}

#cat_header {
    display: flex;
    justify-content: space-between;
}

.actions {
    display: flex;
    justify-content: flex-end;
}

.scroll-container {
    display: flex;
    align-items: center;
}

.scroll-wrapper {
    overflow-x: auto;
    flex: 1;
}

.scroll-content {
    display: flex;
}

.item {
    flex: 0 0 auto;
    margin-right: 10px;
    /* Adjust the margin between items as needed */
    background-color: #998181;
    /* Dark background color */
    color: #fff;
    /* Text color */
    display: flex;
    justify-content: center;
    align-items: center;
}

.scroll-button {
    background-color: #46484e;
    height: 100px;
    color: #fff;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.scroll-button:hover {
    background-color: #555;
    /* Hover background color */
}

.scroll-button:active {
    transform: translateY(1px);
    /* Add a small vertical shift when clicked */
}
</style>