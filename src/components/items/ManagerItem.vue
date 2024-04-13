<template>
  <base-dialog :show="!!error" title="Error occured" @close="closeError">
    <p>{{ error }}</p>
  </base-dialog>
  <li>
    <h3>{{ itemName }}</h3>
    <h5>Rate : Rs. {{ rate }}</h5>
    <h5>Quantity Available : {{ quantity }}</h5>
    <div class="actions">
      <base-button link :to="editItem">Edit</base-button>
      <base-button mode="red" @click="deleteItem()">Delete</base-button>
    </div>
  </li>
</template>

<script>
export default {
  props: ["id", "itemName", "rate", "quantity", "cat_id"],
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
        await this.$store.dispatch('manager_items/deleteItem', {
          id: this.id
        })
      } catch (err) {
        this.error = err.message || "Failed to delete"
      }
    }
  },
  computed: {
    editItem() {
      return "/manager/" + this.cat_id + "/edit/"+ this.id;
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
  list-style: none;
  margin: 14px;
}

h3 {
  font-size: 1.3rem;
}

h3,
h4 {
  margin: 0.5rem 0;
}

div {
  margin: 0.5rem 0;
}

.actions {
  display: flex;
  justify-content: flex-end;
}
</style>