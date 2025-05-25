<script setup>
import { onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const { uidb64, token } = route.params
  try {
    await axios.get(`/api/activate/${uidb64}/${token}/`)
    router.push('/email-verified')
  } catch {
    router.push('/email-verify-failed')
  }
})
</script>

<template>
  <div class="container text-center mt-5">
    <p>🔄 이메일 인증 중입니다...</p>
  </div>
</template>
