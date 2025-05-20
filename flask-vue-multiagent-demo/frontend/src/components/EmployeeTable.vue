<template>
  <v-card>
    <v-data-table :items="employees" :headers="headers" class="elevation-1" />
  </v-card>
</template>

<script setup>
const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Name', key: 'name' },
  { title: 'Salary', key: 'salary' },
  { title: 'Country', key: 'country' },
  { title: 'City', key: 'city' }
]

const employees = [
  { id: 1, name: 'John', salary: '$36,738', country: 'USA', city: 'New York' },
  { id: 2, name: 'Jane', salary: '$23,789', country: 'Canada', city: 'Toronto' },
  { id: 3, name: 'Alice', salary: '$45,846', country: 'UK', city: 'London' },
  { id: 4, name: 'Bob', salary: '$29,345', country: 'Germany', city: 'Berlin' },
  { id: 5, name: 'Eve', salary: '$32,987', country: 'France', city: 'Paris' }
]
</script>

<style scoped>
</style>
