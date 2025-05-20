<template>
  <v-app>
    <Sidebar />
    <Navbar />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

export default defineComponent({
  components: { Sidebar, Navbar }
})
</script>
