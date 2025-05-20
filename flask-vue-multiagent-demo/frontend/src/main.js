import { createApp } from 'vue'
import App from './App.vue'

<<<<<<< HEAD
// Vuetify関係のインポート
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'


const app = createApp(App)

import('https://cdn.jsdelivr.net/npm/vuetify@3/dist/vuetify.esm.js')
  .then(({ createVuetify }) => {
    const vuetify = createVuetify({
  components,
  directives,
})
    app.use(vuetify)
    app.mount('#app')
  })
  .catch(() => {
    app.mount('#app')
  })
=======
createApp(App).mount('#app')

>>>>>>> 11169b6f4abdde79ac9f26e0186dadc485cd3c4d
