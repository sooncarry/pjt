<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const uidb64 = route.params.uidb64
const token = route.params.token

const form = ref({
  username: '',
  first_name: '',
  password: '',
  passwordConfirm: '',
  phone_number: ''
})

const alertMsg = ref('')
const alertType = ref('')

const handleSubmit = async () => {
  if (form.value.password !== form.value.passwordConfirm) {
    alertMsg.value = '❌ 비밀번호가 일치하지 않습니다.'
    alertType.value = 'danger'
    return
  }

  try {
    const res = await axios.post('/api/final-signup/', {
      uidb64,
      token,
      username: form.value.username,
      first_name: form.value.first_name,
      password: form.value.password,
      phone_number: form.value.phone_number
    })
    alertMsg.value = res.data.message || '회원가입 완료! 로그인 페이지로 이동합니다.'
    alertType.value = 'success'
    setTimeout(() => router.push('/login'), 2000)
  } catch (err) {
    console.error(err)
    alertMsg.value = '❌ 오류: ' + (err.response?.data?.error || '회원가입 실패')
    alertType.value = 'danger'
  }
}
</script>

<template>
  <div class="container my-5" style="max-width: 500px;">
    <h2 class="mb-4 text-center">👤 추가 회원 정보 입력</h2>
    <div v-if="alertMsg" :class="['alert', alertType === 'success' ? 'alert-success' : 'alert-danger']">
      {{ alertMsg }}
    </div>

    <form @submit.prevent="handleSubmit" class="d-flex flex-column gap-3">
      <input v-model="form.username" type="text" class="form-control" placeholder="아이디" required />
      <input v-model="form.first_name" type="text" class="form-control" placeholder="이름" required />
      <input v-model="form.phone_number" type="tel" class="form-control" placeholder="전화번호 (선택)" />
      <input v-model="form.password" type="password" class="form-control" placeholder="비밀번호" required />
      <input v-model="form.passwordConfirm" type="password" class="form-control" placeholder="비밀번호 확인" required />
      <button type="submit" class="btn btn-primary mt-3">회원가입 완료</button>
    </form>
  </div>
</template>
