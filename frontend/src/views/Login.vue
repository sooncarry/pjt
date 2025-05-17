<template>
  <div class="login">
    <h1>로그인</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>아이디</label>
        <input v-model="form.username" type="text" required />
      </div>
      <div class="form-group">
        <label>비밀번호</label>
        <input v-model="form.password" type="password" required />
      </div>
      <p class="error" v-if="errorMessage">{{ errorMessage }}</p>
      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'

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

    // axios 기본 Authorization 헤더 설정
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`

    // ✅ 홈으로 이동 + 새로고침
    window.location.href = '/'
  } catch (err) {
    errorMessage.value = '로그인 실패: 아이디 또는 비밀번호를 확인하세요.'
    console.error(err)
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: auto;
  padding: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

input {
  padding: 0.5rem;
  font-size: 1rem;
}

button {
  padding: 0.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  font-size: 1rem;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
</style>
