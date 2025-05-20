<template>
  <v-navigation-drawer app permanent>
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="text-h6">My App</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item v-for="item in items" :key="item.title" link>
        <v-list-item-icon><v-icon>{{ item.icon }}</v-icon></v-list-item-icon>
        <v-list-item-content><v-list-item-title>{{ item.title }}</v-list-item-title></v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Sidebar',
  setup() {
    const items = [
      { title: 'Dashboard', icon: 'mdi-view-dashboard' },
      { title: 'User Profile', icon: 'mdi-account' },
      { title: 'Table List', icon: 'mdi-table' },
      { title: 'Typography', icon: 'mdi-format-size' },
      { title: 'Icons', icon: 'mdi-emoticon' },
      { title: 'Maps', icon: 'mdi-map' },
      { title: 'Notifications', icon: 'mdi-bell' }
    ]
    return { items }
  }
})
</script>
