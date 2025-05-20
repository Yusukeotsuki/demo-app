<template>
  <v-navigation-drawer app permanent width="240" color="grey-lighten-4">
    <v-list>
      <v-list-item class="text-h6 font-weight-bold">Vuetify MD</v-list-item>
      <v-divider class="mb-2" />
      <v-list-item
        v-for="item in items"
        :key="item.title"
        :prepend-icon="item.icon"
        :title="item.title"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
const items = [
  { title: 'Dashboard', icon: 'mdi-view-dashboard' },
  { title: 'User Profile', icon: 'mdi-account' },
  { title: 'Table List', icon: 'mdi-table' },
  { title: 'Typography', icon: 'mdi-format-text' },
  { title: 'Icons', icon: 'mdi-emoticon' },
  { title: 'Maps', icon: 'mdi-map' },
  { title: 'Notifications', icon: 'mdi-bell' }
]
</script>

<style scoped>
</style>
