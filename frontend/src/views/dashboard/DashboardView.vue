<template>
  <div style="padding: 2rem">
    <Button label="Logout" severity="danger" @click="logout" />
  </div>
</template>

<script setup>
import Button from 'primevue/button'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>