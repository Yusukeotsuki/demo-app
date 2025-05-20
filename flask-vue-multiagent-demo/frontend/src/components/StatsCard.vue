<template>
  <v-card class="pa-4 d-flex align-center" :color="color" height="100%">
    <v-icon class="mr-4" size="36">{{ icon }}</v-icon>
    <div>
      <div class="text-h6">{{ label }}</div>
      <div class="text-h5 font-weight-bold">{{ value }}</div>
      <div class="text-caption">{{ note }}</div>
    </div>
  </v-card>
</template>

<script setup>
const props = defineProps({
  icon: String,
  label: String,
  value: [String, Number],
  note: String,
  color: { type: String, default: 'white' }
})
</script>

<style scoped>
</style>
