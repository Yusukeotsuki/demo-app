<template>
  <v-card>
    <v-card-title :style="{ backgroundColor: color, color: '#fff' }">
      {{ title }}
    </v-card-title>
    <v-card-text>
      <canvas ref="canvas"></canvas>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { Chart, ChartData, ChartOptions } from 'chart.js'

export default defineComponent({
  name: 'ChartCard',
  props: {
    title: { type: String, required: true },
    chartType: { type: String as () => 'line' | 'bar', required: true },
    chartData: { type: Object as () => ChartData, required: true },
    chartOptions: { type: Object as () => ChartOptions, required: true },
    color: { type: String, required: true }
  },
  setup(props) {
    const canvas = ref<HTMLCanvasElement | null>(null)

    onMounted(() => {
      if (canvas.value) {
        new Chart(canvas.value, {
          type: props.chartType,
          data: props.chartData,
          options: props.chartOptions
        })
      }
    })

    return { canvas }
  }
})
</script>
