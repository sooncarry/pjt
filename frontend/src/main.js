import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/custom.scss'

axios.defaults.baseURL = 'http://localhost:8000'

// ✅ 토큰이 없거나 잘못된 경우 Authorization 헤더 삭제
const token = localStorage.getItem('access_token')
if (token && token !== 'undefined' && token !== 'null') {
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
} else {
  delete axios.defaults.headers.common['Authorization']
}

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
