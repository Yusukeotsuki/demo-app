<template>
  <v-card :color="color" class="pa-4" height="100%">
    <v-card-title>{{ title }}</v-card-title>
    <v-card-subtitle>{{ subtitle }}</v-card-subtitle>
    <component
      :is="chartTag"
      :data="chartData"
      :options="chartOptions"
      class="chart"
    />
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { Bar, Line } from 'vue-chartjs'

const props = defineProps({
  title: String,
  subtitle: String,
  chartData: Object,
  chartOptions: Object,
  type: { type: String, default: 'line' },
  color: { type: String, default: 'white' }
})

const chartTag = computed(() => (props.type === 'bar' ? Bar : Line))
</script>

<style scoped>
.chart {
  height: 200px;
}
</style>
