import  piniaPluginPersistedstate  from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// import BootstrapVue3 from 'bootstrap-vue-3'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

const app = createApp(App)
const pinia = createPinia()


pinia.use(piniaPluginPersistedstate)
// app.use(createPinia())
app.use(pinia)
app.use(router)


// VueElement.use(bootstrapVue)
app.mount('#app')
