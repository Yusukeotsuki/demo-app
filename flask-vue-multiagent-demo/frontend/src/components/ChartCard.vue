<template>
  <div class="chart-card">
    <canvas ref="canvas" width="200" height="40"></canvas>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
export default {
  props: {
    chartData: Number
  },
  setup(props) {
    const canvas = ref(null)
    onMounted(() => {
      if (canvas.value) {
        const ctx = canvas.value.getContext('2d')
        ctx.fillStyle = '#4caf50'
        const width = Math.min(props.chartData || 0, 100) * 2
        ctx.fillRect(0, 0, width, 40)
      }
    })
    return { canvas }
  }
}
</script>

<style scoped>
.chart-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>
