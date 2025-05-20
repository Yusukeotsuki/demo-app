<template>
  <v-card>
    <v-data-table :headers="headers" :items="items" class="elevation-1" />
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'EmployeeTable',
  props: {
    items: {
      type: Array as () => Array<{ id: number | string; name: string; salary: string; country: string; city: string }>,
      required: true
    }
  },
  setup() {
    const headers = [
      { text: 'ID', value: 'id' },
      { text: 'Name', value: 'name' },
      { text: 'Salary', value: 'salary' },
      { text: 'Country', value: 'country' },
      { text: 'City', value: 'city' }
    ]
    return { headers }
  }
})
</script>
