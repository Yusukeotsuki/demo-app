<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4">
        <ChartCard
          title="Daily Sales"
          chartType="line"
          :chartData="dailySalesData"
          :chartOptions="chartOptions"
          color="#00bcd4"
        />
      </v-col>
      <v-col cols="12" md="4">
        <ChartCard
          title="Email Subscription"
          chartType="bar"
          :chartData="emailData"
          :chartOptions="chartOptions"
          color="#f44336"
        />
      </v-col>
      <v-col cols="12" md="4">
        <ChartCard
          title="Completed Tasks"
          chartType="line"
          :chartData="tasksData"
          :chartOptions="chartOptions"
          color="#4caf50"
        />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <StatCard icon="mdi-chart-bar" label="Revenue" value="$34,245" description="Last 24 Hours" />
      </v-col>
      <v-col cols="12" md="3">
        <StatCard icon="mdi-database" label="Used Space" value="49/50 GB" description="Get More Space" />
      </v-col>
      <v-col cols="12" md="3">
        <StatCard icon="mdi-alert-circle" label="Fixed Issues" value="75" description="Tracked from GitHub" />
      </v-col>
      <v-col cols="12" md="3">
        <StatCard icon="mdi-twitter" label="Followers" value="+245" description="Just Updated" />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <EmployeeTable :items="employees" />
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <TaskList :tasks="tasks" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ChartCard from '../components/ChartCard.vue'
import StatCard from '../components/StatCard.vue'
import EmployeeTable from '../components/EmployeeTable.vue'
import TaskList from '../components/TaskList.vue'
import { ChartData, ChartOptions } from 'chart.js'

export default defineComponent({
  name: 'DashboardView',
  components: { ChartCard, StatCard, EmployeeTable, TaskList },
  setup() {
    const chartOptions: ChartOptions = { responsive: true, maintainAspectRatio: false }

    const dailySalesData: ChartData = {
      labels: ['M', 'T', 'W', 'T', 'F', 'S', 'S'],
      datasets: [
        {
          label: 'Sales',
          data: [12, 17, 7, 17, 23, 18, 38],
          borderColor: '#fff',
          backgroundColor: 'rgba(255,255,255,0.5)',
          fill: false
        }
      ]
    }

    const emailData: ChartData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      datasets: [
        {
          label: 'Subscriptions',
          data: [5, 20, 36, 10, 10, 20, 30, 40, 50, 60, 70, 80],
          backgroundColor: 'rgba(255,255,255,0.5)'
        }
      ]
    }

    const tasksData: ChartData = {
      labels: ['12am', '3am', '6am', '9am', '12pm', '3pm', '6pm', '9pm'],
      datasets: [
        {
          label: 'Tasks',
          data: [230, 750, 450, 300, 280, 240, 200, 190],
          borderColor: '#fff',
          backgroundColor: 'rgba(255,255,255,0.5)',
          fill: false
        }
      ]
    }

    const employees = [
      { id: 1, name: 'Dakota Rice', salary: '$36,738', country: 'Niger', city: 'Oud-Turnhout' },
      { id: 2, name: 'Minerva Hooper', salary: '$23,789', country: 'Curaçao', city: 'Sinaai-Waas' },
      { id: 3, name: 'Sage Rodriguez', salary: '$56,142', country: 'Netherlands', city: 'Baileux' },
      { id: 4, name: 'Philip Chaney', salary: '$38,735', country: 'Korea, South', city: 'Overland Park' }
    ]

    const tasks = [
      { text: 'Sign contract for what?', type: 'Bugs' },
      { text: 'Create new landing page', type: 'Website' },
      { text: 'Update server configuration', type: 'Server' }
    ]

    return { chartOptions, dailySalesData, emailData, tasksData, employees, tasks }
  }
})
</script>
