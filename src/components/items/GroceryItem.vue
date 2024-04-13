<template>
  <base-dialog :show="!!error" title="Error occured" @close="closeError">
    <p>{{ error }}</p>
  </base-dialog>
  <li>
    <h3>{{ itemName }}</h3>
    <h5>Rate : Rs. {{ rate }}</h5>
    <h5>Quantity Available : {{ quantity }}</h5>
    <div class="actions">
      <button id="out_of_stock" v-if="outOfStock">Out of stock</button>
      <base-button v-else link :to="addToCart">Buy</base-button>
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
  },
  computed: {
    outOfStock(){
      return this.quantity == 0;
    },
    addToCart() {
      return "/items/" + this.cat_id + "/add_to_cart/" + this.id;
    }
  }
}
</script>

<style scoped>
li {
  margin: 1rem 0;
  width: 13rem;
  border: 1px solid #424242;
  border-radius: 12px;
  padding: 1rem;
  background-color: rgba(25, 29, 29, 0.7);
  list-style: none;
  margin: 14px;
}
#out_of_stock{
  /* width:100rem; */
  color: white;
  background-color: rgb(182, 0, 0);
  /* border-radius: 10px; */
  border: 1px solid  rgb(182, 0, 0);
  border-radius: 13px;
  margin-right: 5px;
  height: 40px;

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