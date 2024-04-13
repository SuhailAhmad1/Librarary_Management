<template>
    <div class="card">
        <slot></slot>
    </div>
</template>

<style scoped>
.card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.26);
  background-color: rgba(37, 27, 27, 0.5);
  padding: 1rem;
  margin: 2rem auto;
  color: white;
  max-width: 40rem;
}
</style>