<template>
  <!-- NAVBAR 아래 여백 확보 (조금 더 내려서 120px) -->
  <div class="container my-5 d-flex justify-content-center" style="padding-top: 120px;">
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

        <!-- 버튼 둘을 가로로 나란히 배치 -->
        <div class="d-flex gap-2 mt-2">
          <!-- 로그인: 좌측 절반 -->
          <button
            type="submit"
            class="btn btn-primary rounded-pill flex-fill"
          >
            로그인
          </button>
          <!-- 회원가입: 우측 절반 -->
          <button
            type="button"
            class="btn btn-outline-secondary rounded-pill flex-fill"
            @click="goSignup"
          >
            회원가입
          </button>
        </div>
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

    // 홈으로 이동 (새로고침)
    window.location.href = '/'
  } catch (err) {
    errorMessage.value = '❌ 로그인 실패: 아이디 또는 비밀번호를 확인하세요.'
    console.error(err)
  }
}

// 회원가입으로 이동하는 메서드
const goSignup = () => {
  router.push({ name: 'Signup' }) // 또는 path: '/signup'
}
</script>

<style scoped>
/* 필요 시 추가 스타일만 */
</style>
