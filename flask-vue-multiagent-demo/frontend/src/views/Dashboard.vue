<template>
  <v-app>
    <Sidebar />
    <v-main>
      <Topbar />
      <v-container fluid>
        <v-row>
          <v-col cols="12" md="4" v-for="(chart, i) in charts" :key="i">
            <ChartCard
              :title="chart.title"
              :subtitle="chart.subtitle"
              :chartData="chart.data"
              :chartOptions="chart.options"
              :type="chart.type"
              :color="chart.color"
            />
          </v-col>
        </v-row>
        <v-row class="mt-4">
          <v-col cols="12" md="3" v-for="(stat, i) in stats" :key="i">
            <StatsCard
              :icon="stat.icon"
              :label="stat.label"
              :value="stat.value"
              :note="stat.note"
              :color="stat.color"
            />
          </v-col>
        </v-row>
        <v-row class="mt-4">
          <v-col cols="12" md="6">
            <EmployeeTable />
          </v-col>
          <v-col cols="12" md="6">
            <TaskList />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import Sidebar from '../components/Sidebar.vue'
import Topbar from '../components/Topbar.vue'
import ChartCard from '../components/ChartCard.vue'
import StatsCard from '../components/StatsCard.vue'
import EmployeeTable from '../components/EmployeeTable.vue'
import TaskList from '../components/TaskList.vue'

const charts = [
  {
    title: 'Sales',
    subtitle: 'Last Week',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{ data: [40, 39, 10, 40, 39, 80, 40], label: 'Sales' }]
    },
    options: {},
    type: 'line',
    color: 'light-blue lighten-4'
  },
  {
    title: 'Revenue',
    subtitle: 'This Month',
    data: {
      labels: ['W1', 'W2', 'W3', 'W4'],
      datasets: [{ data: [400, 200, 300, 500], label: 'Revenue' }]
    },
    options: {},
    type: 'bar',
    color: 'pink lighten-4'
  },
  {
    title: 'Users',
    subtitle: 'Online',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [{ data: [30, 60, 35, 50, 49, 60, 70], label: 'Users' }]
    },
    options: {},
    type: 'line',
    color: 'green lighten-4'
  }
]

const stats = [
  { icon: 'mdi-account', label: 'Users', value: 1234, note: '+3% from last week', color: 'blue lighten-5' },
  { icon: 'mdi-cash', label: 'Revenue', value: '$23k', note: '+10% from last month', color: 'red lighten-5' },
  { icon: 'mdi-cart', label: 'Orders', value: 320, note: '5 new today', color: 'green lighten-5' },
  { icon: 'mdi-chart-bar', label: 'Visits', value: '1.2k', note: 'stable', color: 'orange lighten-5' }
]
</script>

<style scoped>
</style>
