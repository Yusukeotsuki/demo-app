<template>
  <div class="stat-card">
    <h3>{{ title }}</h3>
    <p>{{ value }}</p>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    value: [String, Number]
  }
}
</script>

<style scoped>
.stat-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stat-card h3 {
  margin: 0 0 8px;
}
</style>
