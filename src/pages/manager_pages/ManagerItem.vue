<template>
    <the-manager-header></the-manager-header>
    <base-dialog :show="!!error" title="An error occured!" @close="closeError">
        <p>{{ error }}</p>
    </base-dialog>
    <section>
        <div class="controls">
            <div id="left-controls">
                <input type="text" v-model="searchTerm" placeholder="Search products...">
                <base-button mode="outline" link :to="addItem">+ Add Category</base-button>
            </div>

            <div id="right-controls">
                <button :disabled="generation_state == 'PENDING'">
                <div v-if="generation_state == 'PENDING'" disabled>Generating......</div>
                <div v-else-if="generation_state == 'SUCCESS'" disabled @click="downloadCsv()">Download CSV</div>
                <div v-else @click="triggerGeneration">Generate CSV</div>
            </button>
            </div>
            
        </div>
        <div v-if="isLoading">
            <base-spinner></base-spinner>
        </div>

        <ul v-else-if="allManagerItems.length">
            <category-item v-for="cat in allManagerItems" :key="cat.id" :id="cat.cat_id" :cat_name="cat.cat_name"
                :products="cat.products"></category-item>
        </ul>
        <h2 v-else>No items Found</h2>
    </section>
</template>

<script>
import CategoryItem from '../../components/items/CategoryItem.vue';
import TheManagerHeader from '../../components/layout/TheManagerHeader.vue'
export default ({
    components: {
        CategoryItem,
        TheManagerHeader
    },
    data() {
        return {
            searchTerm: "",
            isLoading: false,
            generation_state: "",
            gen_task_id: "",
            pollIntervalId: "",
            csv_data: null,
            error: null
        };
    },
    methods: {
        async downloadCsv() {
            const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/download_csv", {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("token")}`,
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "csv_data": this.csv_data })
            })

            if (!response.ok) {
                const error = new Error('Failed to get Graph Items.')
                throw error;
            }
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'product.csv'; // Specify the filename and extension
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url); // Clean up
        },

        async triggerGeneration() {
            this.generation_state = "PENDING"
            const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/generate_csv", {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem("token")}`
                }
            })

            if (!response.ok) {
                const error = new Error('Failed to get Graph Items.')
                throw error;
            }
            const responseData = await response.json();
            this.gen_task_id = responseData.data
            this.pollIntervalId = setInterval(this.checkTaskStatus, 2000);
        },

        async checkTaskStatus() {
            try {
                const response = await fetch(process.env.VUE_APP_BACKEND_URL + "/api/manager/get_generate_task_status/" + this.gen_task_id, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("token")}`
                    }
                })

                if (!response.ok) {
                    const error = new Error('Failed to get Graph Items.')
                    throw error;
                }
                const responseData = await response.json();

                this.generation_state = responseData.status
                console.log(this.generation_state)
                if (responseData.status === "SUCCESS" || responseData.status === "FAILURE") {
                    this.csv_data = responseData.result
                    clearInterval(this.pollIntervalId); // Stop polling if task is completed
                }
            } catch (error) {
                console.error("Error checking task status:", error);
            }
        },

        closeError() {
            this.error = null;
        },
    },
    computed: {
        allManagerItems() {
            const allItems = this.$store.getters['manager_items/managerItems']
            console.log(allItems)
            const term = this.searchTerm.toLowerCase().trim();
            if (!term) return allItems

            return allItems.map(category => {
                const matchingProducts = category.products.filter(product =>
                    product.itemName.toLowerCase().includes(term)
                );
                return { ...category, products: matchingProducts };
            }).filter(category => category.products.length > 0);
        },
        hasItems() {
            return this.$store.getters['manager_items/hasItem']
        },
        addItem() {
            return "/manager/addCategory"
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
})
</script>

<style scoped>
ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.controls {
    display: flex;
    margin-left: 0.7rem;
    justify-content: space-between;
}

.controls button {
    font-size: 1rem;
    padding: 10px;
    border-radius: 30px;
    border: 0px;
    background-color: rgb(0, 168, 126);
    color: white;
}

.controls button:hover {
    color: rgb(255, 254, 254);
    background-color: rgb(19, 105, 58);
}

#left-controls{
    margin-left: 10px
}

#right-controls{
    margin-right: 30px;
}

input {
    height: 95%;
    margin-right: 30px;
    border-radius: 10px;
}

section {
    margin: 2rem;
}
</style>