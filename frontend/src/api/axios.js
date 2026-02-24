import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
})

api.interceptors.request.use((config) => {
  const authStore = useAuthStore()

  if (authStore.accessToken) {
    config.headers.Authorization = `Bearer ${authStore.accessToken}`
  }

  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    const authStore = useAuthStore()

    if (error.response?.status === 401 && authStore.refreshToken) {
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/api/token/refresh/',
          { refresh: authStore.refreshToken }
        )

        authStore.accessToken = response.data.access
        localStorage.setItem('access', response.data.access)

        error.config.headers.Authorization = `Bearer ${response.data.access}`

        return axios(error.config)

      } catch (refreshError) {
        authStore.logout()
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export default api