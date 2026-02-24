<template>
  <div class="flex justify-content-center align-items-center" style="height: 100vh">
    <Card style="width: 400px">
      <template #title>Login</template>

      <template #content>
        <div class="field mb-4">
          <FloatLabel>
            <InputText id="username" v-model="username" class="w-full" />
            <label for="username">Username</label>
          </FloatLabel>
        </div>

        <div class="field mb-4">
          <FloatLabel>
            <Password id="password" v-model="password" toggleMask class="w-full" />
            <label for="password">Password</label>
          </FloatLabel>
        </div>

        <Message v-if="errorMessage" severity="error" class="mb-3">
          {{ errorMessage }}
        </Message>

        <Button
          label="Login"
          class="w-full"
          :loading="loading"
          @click="handleLogin"
        />
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from 'primevue/card'
import FloatLabel from 'primevue/floatlabel'
import Message from 'primevue/message'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'

const username = ref('')
const password = ref('')
const router = useRouter()
const authStore = useAuthStore()

const errorMessage = ref('')
const loading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (error) {
    errorMessage.value = 'Invalid username or password'
  } finally {
    loading.value = false
  }
}
</script>