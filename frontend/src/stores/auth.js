import { defineStore } from 'pinia'
import axios from 'axios'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access') || null,
    refreshToken: localStorage.getItem('refresh') || null,
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(username, password) {
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/api/token/',
          { username, password }
        )

        this.accessToken = response.data.access
        this.refreshToken = response.data.refresh

        localStorage.setItem('access', this.accessToken)
        localStorage.setItem('refresh', this.refreshToken)

      } catch (error) {
        throw error
      }
    },

    logout() {
      this.accessToken = null
      this.refreshToken = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },
  },
})