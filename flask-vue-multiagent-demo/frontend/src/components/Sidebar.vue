<template>
  <div class="sidebar">
    <img src="../assets/logo.png" alt="Logo" class="logo" />
    <ul>
      <li>Home</li>
      <li>Analytics</li>
      <li>Settings</li>
    </ul>
  </div>
</template>

<script>
export default {}
</script>

<style scoped>
.sidebar {
  width: 200px;
  background: #333;
  color: #fff;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}
.logo {
  width: 100%;
  margin-bottom: 20px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
  cursor: pointer;
}
</style>
