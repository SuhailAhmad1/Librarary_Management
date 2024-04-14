<template>
  <the-header></the-header>
  <base-dialog :show="!!error" title="An error occured!" @close="handleError">
    <p>{{ error }}</p>
  </base-dialog>
  <section>
    <h2>All Books</h2>
    <div class="controls">
      <input type="text" v-model="searchTerm" placeholder="Search products...">
      <base-button mode="outline" @click="loadItems()">Refresh</base-button>
    </div>

    <div v-if="isLoading">
      <base-spinner></base-spinner>
    </div>

    <ul v-else-if="allItems.length">
      <category-itemuser v-for="cat in allItems" :key="cat.id" :id="cat.cat_id" :cat_name="cat.cat_name" 
        :products="cat.products"></category-itemuser>
    </ul>
    <h2 v-else>No items Found</h2>
  </section>
</template>

<script>
import TheHeader from '../../components/layout/TheHeader.vue';
import CategoryItemuser from "../../components/items/CategoryItemuser.vue";

export default {
  components: {
    CategoryItemuser,
    TheHeader
  },
  data() {
    return {
      searchTerm: "",
      isLoading: false,
      error: null
    };
  },

  computed: {
    allItems() {
      const allItems = this.$store.getters['items/items'];
      const term = this.searchTerm.toLowerCase().trim();
      if (!term) return allItems

      return allItems.map(category => {
        const matchingProducts = category.products.filter(product =>
          product.itemName.toLowerCase().includes(term)
        );
        console.log(term)
        return { ...category, products: matchingProducts };
      }).filter(category => category.products.length > 0);
    }
  },

  methods: {
    handleError() {
      this.error = null
    },
    async loadItems() {
      this.isLoading = true
      try {
        await this.$store.dispatch('items/loadItems', { forceRefresh: true })
      } catch (error) {
        this.error = error.message || 'Something went wrong'
      }
      this.isLoading = false
    }
  },
  created() {
    this.loadItems()
  }
};
</script>

<style scoped>
h2{
  font-size: 30px;
  text-align: center;
}
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.controls {
  display: flex;
  margin-left: 0.8rem;
}

input {
  margin-right: 30px;
  border-radius: 10px;
}

section {
  margin: 2rem;
}
</style>