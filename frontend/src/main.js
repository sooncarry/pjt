import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

// main.js
import 'bootstrap/dist/css/bootstrap.min.css'   // ← 필수!
import './assets/custom.scss'                   // ← SCSS 커스터마이징 했다면!


axios.defaults.baseURL = 'http://localhost:8000'
const token = localStorage.getItem('access_token')
if (token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')