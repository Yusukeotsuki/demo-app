<template>
  <v-card class="pa-4">
    <div class="d-flex align-center">
      <v-avatar size="40" class="mr-4" color="primary">
        <v-icon dark>{{ icon }}</v-icon>
      </v-avatar>
      <div>
        <div class="text-subtitle-1">{{ label }}</div>
        <div class="text-h5 font-weight-bold">{{ value }}</div>
      </div>
    </div>
    <v-card-text class="pt-2">{{ description }}</v-card-text>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'StatCard',
  props: {
    icon: { type: String, required: true },
    label: { type: String, required: true },
    value: { type: [String, Number], required: true },
    description: { type: String, required: true }
  }
})
</script>
