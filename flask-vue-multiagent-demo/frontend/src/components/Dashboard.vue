<template>
  <div class="dashboard">
    <Sidebar />
    <div class="content">
      <div class="stats">
        <StatCard title="Users" :value="123" />
        <StatCard title="Sales" :value="456" />
      </div>
      <ChartCard :chartData="75" />
    </div>
  </div>
</template>

<script>
import Sidebar from './Sidebar.vue'
import StatCard from './StatCard.vue'
import ChartCard from './ChartCard.vue'

export default {
  components: { Sidebar, StatCard, ChartCard }
}
</script>

<style scoped>
.dashboard {
  display: flex;
}
.content {
  flex: 1;
  padding: 20px;
}
.stats {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
</style>
