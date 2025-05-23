import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({}),
  getters: {
    isLoggedIn: () => !!localStorage.getItem('access_token'),
  },
  actions: {
    login(token) {
      localStorage.setItem('access_token', token)
    },
    logout() {
      localStorage.removeItem('access_token')
    },
  },
})
