<template>
  <div class="container my-5 d-flex justify-content-center">
    <div class="card p-4 shadow-sm border-0 rounded-4" style="max-width: 400px; width: 100%;">
      <h1 class="fw-bold mb-4 text-center">🔐 로그인</h1>

      <form @submit.prevent="handleLogin" class="d-flex flex-column gap-3">
        <div>
          <label class="form-label">아이디</label>
          <input
            v-model="form.username"
            type="text"
            class="form-control form-control-sm"
            required
          />
        </div>

        <div>
          <label class="form-label">비밀번호</label>
          <input
            v-model="form.password"
            type="password"
            class="form-control form-control-sm"
            required
          />
        </div>

        <div v-if="errorMessage" class="text-danger small">{{ errorMessage }}</div>

        <button type="submit" class="btn btn-primary btn-sm rounded-pill mt-2">
          로그인
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
const router = useRouter()

const form = reactive({
  username: '',
  password: ''
})

const errorMessage = ref('')

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    const response = await axios.post('/api/token/', {
      username: form.username,
      password: form.password
    })

    // 토큰 저장
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)
    localStorage.setItem('username', form.username)

    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

    // ✅ 홈으로 이동 + 새로고침
    window.location.href = '/'
  } catch (err) {
    errorMessage.value = '❌ 로그인 실패: 아이디 또는 비밀번호를 확인하세요.'
    console.error(err)
  }
}
</script>

<style scoped>
/* 필요 시 추가 스타일만 */
</style>
