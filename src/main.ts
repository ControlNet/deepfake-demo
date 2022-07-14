import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { BootstrapVue3 } from "bootstrap-vue-3";
// @ts-ignore
import VuePlyr from 'vue-plyr'

import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-vue-3/dist/bootstrap-vue-3.css"
import 'vue-plyr/dist/vue-plyr.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(BootstrapVue3)
app.use(VuePlyr)

app.mount('#app')
