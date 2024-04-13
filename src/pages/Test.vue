<template>
    <div class="scroll-container">
        <button class="scroll-button" @click="scrollLeft">&lt;</button>
        <div class="scroll-wrapper" ref="scrollWrapper">
            <div class="scroll-content">
                <div v-for="(item, index) in items" :key="index" class="item">{{ item }}</div>
            </div>
        </div>
        <button class="scroll-button" @click="scrollRight">&gt;</button>
    </div>
    <div class="scroll-container">
        <button class="scroll-button" @click="scrollLeft">&lt;</button>
        <div class="scroll-wrapper" ref="scrollWrapper">
            <div class="scroll-content">
                <manager-item v-for="item in allManagerItems[1].products" :key="item.id" :id="item.id" :itemName="item.itemName"
                    :rate="item.rate" :quantity="item.quantity" :category="item.category" class="item"></manager-item>
            </div>
        </div>
        <button class="scroll-button" @click="scrollRight">&gt;</button>
    </div>
</template>

<script>
import ManagerItem from "../components/items/ManagerItem.vue"

export default {
    components: {
        ManagerItem
    },
    data() {
        return {
            items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], // Example array of items
            scrollStep: 200, // Pixels to scroll on each button click
            isLoading: false,
            error: null
        };
    },
    methods: {
        closeError() {
            this.error = null;
        },
        scrollLeft() {
            this.$refs.scrollWrapper.scrollLeft -= this.scrollStep;
        },
        scrollRight() {
            this.$refs.scrollWrapper.scrollLeft += this.scrollStep;
        }
    },
    computed: {
        allManagerItems() {
            return this.$store.getters['manager_items/managerItems']
        },
        hasItems() {
            return this.$store.getters['manager_items/hasItem']
        },
        addItem() {
            return "/manager/addItem"
        }
    },
    async created() {
        try {
            await this.$store.dispatch('manager_items/setAPIdata');
        } catch (err) {
            console.log('I am here .....')
            this.error = err.message || "Failed to load"
        }
    }
};
</script>

<style>
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
    width: 200px;
    /* Adjusted width */
    height: 200px;
    /* Adjusted height */
    margin-right: 10px;
    /* Adjust the margin between items as needed */
    background-color: #444;
    /* Dark background color */
    color: #fff;
    /* Text color */
    display: flex;
    justify-content: center;
    align-items: center;
}

.scroll-button {
    background-color: #333;
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