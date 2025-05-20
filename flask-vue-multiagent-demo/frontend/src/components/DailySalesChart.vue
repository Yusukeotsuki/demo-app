<template>
  <div class="daily-sales-card">
    <h3 class="title">Daily Sales</h3>
    <canvas ref="canvas" class="chart-canvas"></canvas>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue'
import { Chart, type ChartData, type ChartOptions } from 'chart.js/auto'

interface Props {
  chartData: ChartData<'line'>
  chartOptions?: ChartOptions<'line'>
}

const props = defineProps<Props>()

const canvas = ref<HTMLCanvasElement | null>(null)
let chart: Chart<'line'> | null = null

const renderChart = () => {
  if (!canvas.value) return
  if (chart) {
    chart.destroy()
  }
  chart = new Chart(canvas.value, {
    type: 'line',
    data: props.chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      ...(props.chartOptions || {})
    }
  })
}

onMounted(renderChart)

watch(
  () => [props.chartData, props.chartOptions],
  renderChart,
  { deep: true }
)
</script>

<style scoped>
.daily-sales-card {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
.title {
  margin-bottom: 8px;
  font-weight: 600;
}
.chart-canvas {
  flex: 1;
}
</style>

