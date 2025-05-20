<template>
  <v-card>
    <v-list>
      <v-list-item v-for="(task, i) in tasks" :key="i" :class="typeClass(task.type)">
        <v-list-item-action>
          <v-checkbox v-model="task.done" />
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>{{ task.text }}</v-list-item-title>
        </v-list-item-content>
        <v-list-item-action class="d-flex">
          <v-icon small class="mr-2">mdi-pencil</v-icon>
          <v-icon small>mdi-close</v-icon>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'TaskList',
  props: {
    tasks: {
      type: Array as () => Array<{ text: string; type: 'Bugs' | 'Website' | 'Server'; done?: boolean }>,
      required: true
    }
  },
  setup() {
    const typeClass = (type: string) => {
      if (type === 'Bugs') return 'red'
      if (type === 'Website') return 'blue'
      return 'green'
    }
    return { typeClass }
  }
})
</script>

<style scoped>
.red .v-icon {
  color: red;
}
.blue .v-icon {
  color: blue;
}
.green .v-icon {
  color: green;
}
</style>
