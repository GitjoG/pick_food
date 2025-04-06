import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import { initAuth } from '@/utils/auth'

Vue.use(ElementUI)
Vue.config.productionTip = false

// Configure axios base URL
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:5000/admin/api'

// Initialize authentication state
initAuth()

// Add request interceptor
axios.interceptors.request.use(config => {
  // Auth token is now handled by initAuth and auth.js
  return config
}, error => {
  return Promise.reject(error)
})

// Add response interceptor
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // Handle common errors
    if (error.response) {
      if (error.response.status === 401) {
        // Unauthorized - redirect to login
        router.push('/login')
      } else if (error.response.status === 403) {
        // Forbidden
        ElementUI.Message.error('没有权限执行此操作')
      } else if (error.response.status === 500) {
        // Server error
        ElementUI.Message.error('服务器错误，请稍后再试')
      }
    } else {
      // Network error
      ElementUI.Message.error('网络错误，请检查您的连接')
    }
    return Promise.reject(error)
  }
)

// Make axios available globally
Vue.prototype.$http = axios

new Vue({
  router,
  render: h => h(App)
}).$mount('#app') 