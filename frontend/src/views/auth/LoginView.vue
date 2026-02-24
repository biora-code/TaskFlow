<template>
  <div style="max-width: 400px; margin: 100px auto">
    <h2>Login</h2>

    <InputText v-model="username" placeholder="Username" class="w-full mb-3" />
    <Password v-model="password" placeholder="Password" class="w-full mb-3" />

    <Button label="Login" @click="handleLogin" class="w-full" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'

const username = ref('')
const password = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (error) {
    alert('Invalid credentials')
  }
}
</script>