<template>
  <v-app-bar app flat color="white">
    <v-spacer></v-spacer>
    <v-text-field
      density="compact"
      hide-details
      variant="solo"
      prepend-inner-icon="mdi-magnify"
      label="Search"
    />
    <v-btn icon="mdi-view-grid" class="mx-2" />
    <v-btn icon class="mx-2">
      <v-badge color="red" content="3" overlap>
        <v-icon>mdi-bell</v-icon>
      </v-badge>
    </v-btn>
    <v-avatar size="32">
      <img src="https://randomuser.me/api/portraits/men/85.jpg" alt="user" />
    </v-avatar>
  </v-app-bar>
</template>

<script setup>
</script>

<style scoped>
</style>
