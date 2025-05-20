<template>
  <v-card>
    <v-tabs v-model="tab" background-color="grey-lighten-4" grow>
      <v-tab v-for="t in tabs" :key="t">{{ t }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>
    <v-list>
      <v-list-item
        v-for="task in filteredTasks"
        :key="task.id"
      >
        <template #prepend>
          <v-checkbox v-model="task.done" hide-details></v-checkbox>
        </template>
        <v-list-item-title :class="{ 'text-decoration-line-through': task.done }">
          {{ task.text }}
        </v-list-item-title>
        <template #append>
          <v-btn icon="mdi-pencil" size="small" class="mr-2" />
          <v-btn icon="mdi-delete" size="small" />
        </template>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'

const tabs = ['Bugs', 'Website', 'Server']
const tab = ref('Bugs')

const tasks = ref([
  { id: 1, category: 'Bugs', text: 'Fix login bug', done: false },
  { id: 2, category: 'Bugs', text: 'Resolve issue #123', done: true },
  { id: 3, category: 'Website', text: 'Update landing page', done: false },
  { id: 4, category: 'Server', text: 'Upgrade dependencies', done: false }
])

const filteredTasks = computed(() =>
  tasks.value.filter(t => t.category === tab.value)
)
</script>

<style scoped>
</style>
