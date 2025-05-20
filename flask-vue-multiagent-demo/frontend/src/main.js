import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

import('https://cdn.jsdelivr.net/npm/vuetify@3/dist/vuetify.esm.js')
  .then(({ createVuetify }) => {
    const vuetify = createVuetify()
    app.use(vuetify)
    app.mount('#app')
  })
  .catch(() => {
    app.mount('#app')
  })
