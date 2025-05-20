<template>
  <v-app-bar app>
    <v-app-bar-nav-icon />
    <v-toolbar-title>Dashboard</v-toolbar-title>
    <v-spacer />
    <v-text-field
      solo
      flat
      hide-details
      prepend-inner-icon="mdi-magnify"
      label="Search"
    />
    <v-btn icon>
      <v-badge color="red" content="4" overlap>
        <v-icon>mdi-account-circle</v-icon>
      </v-badge>
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Navbar'
})
</script>
