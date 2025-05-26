<template>
  <div class="container my-5 d-flex justify-content-center">
    <BaseAlert v-if="alertMsg" :message="alertMsg" :type="alertType" />
    <div class="card p-4 shadow-sm border-0 rounded-4" style="width: 100%; max-width: 600px">
      <h1 class="fw-bold mb-4 text-center">👤 회원가입</h1>

      <form @submit.prevent="handleSubmit" class="d-flex flex-column gap-3">
        <!-- 이름 -->
        <div>
          <label class="form-label">이름</label>
          <input v-model="form.name" type="text" class="form-control form-control-ml" required />
        </div>

        <!-- 아이디 -->
        <div>
          <label class="form-label">아이디</label>
          <div class="d-flex gap-2">
            <input v-model="form.username" type="text" class="form-control form-control-ml" required />
            <button
              type="button"
              class="btn btn-outline-secondary btn-sm"
              @click="checkUsername"
              style="border-color: #ced4da; color: #495057; writing-mode: horizontal-tb; white-space: nowrap;"
            >
              중복 확인
            </button>
          </div>

          <p v-if="usernameStatus === 'available'" class="text-success small mt-1">사용 가능한 아이디입니다.</p>
          <p v-else-if="usernameStatus === 'taken'" class="text-danger small mt-1">이미 사용 중인 아이디입니다.</p>
        </div>

        <!-- 비밀번호 -->
        <div>
          <label class="form-label">비밀번호</label>
          <input v-model="form.password" type="password" class="form-control form-control-ml" required />
          <p
            class="small mt-1"
            :class="isPasswordValid ? 'text-success' : (form.password ? 'text-danger' : '')"
          >
            {{ passwordMessage }}
          </p>
        </div>

        <!-- 비밀번호 확인 -->
        <div>
          <label class="form-label">비밀번호 확인</label>
          <input v-model="form.passwordConfirm" type="password" class="form-control form-control-ml" required />
        </div>

        <!-- 이메일 -->
        <div>
          <label class="form-label">이메일</label>
          <div class="d-flex gap-2">
            <input v-model="form.email" type="email" class="form-control form-control-ml" required />
            <button
              type="button"
              class="btn btn-outline-secondary btn-sm"
              @click="sendEmailVerification"
              style="border-color: #ced4da; color: #495057; writing-mode: horizontal-tb; white-space: nowrap;"
            >
              인증
            </button>
          </div>
        </div>

        <!-- 생년월일 -->
        <div>
          <label class="form-label">생년월일 <span class="text-muted small">(선택)</span></label>
          <div class="d-flex gap-2">
            <select v-model="form.birthYear" class="form-select form-select-ml">
              <option disabled value="">년도</option>
              <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
            </select>
            <select v-model="form.birthMonth" class="form-select form-select-ml">
              <option disabled value="">월</option>
              <option v-for="month in 12" :key="month" :value="month">{{ month }}</option>
            </select>
            <select v-model="form.birthDay" class="form-select form-select-ml">
              <option disabled value="">일</option>
              <option v-for="day in 31" :key="day" :value="day">{{ day }}</option>
            </select>
          </div>
        </div>

        <!-- 전화번호 -->
        <div>
          <label class="form-label">전화번호 <span class="text-muted small">(선택)</span></label>
          <input v-model="form.phone" type="tel" class="form-control form-control-ml" />
        </div>


        <!-- 직업 -->
        <div>
          <label class="form-label">직업</label>
          <select v-model="form.job" class="form-select form-select-ml">
            <option disabled value="">선택하세요</option>
            <option>학생</option>
            <option>회사원</option>
            <option>프리랜서</option>
            <option>무직</option>
            <option>기타</option>
          </select>
        </div>


        <!-- 가입 버튼 -->
        <button type="submit" class="btn btn-primary btn-sm rounded-pill mt-3">가입하기</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, inject, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const alertMsg = inject('alertMsg')
const alertType = inject('alertType')

const currentYear = new Date().getFullYear()
const years = Array.from({ length: 100 }, (_, i) => currentYear - i)

const form = reactive({
  name: '',
  email: '',
  username: '',
  password: '',
  passwordConfirm: '',
  birthYear: '',
  birthMonth: '',
  birthDay: '',
  phone: '',
  job: '',
})

const usernameStatus = ref('')
const emailVerified = ref(false)

const passwordMessage = computed(() => {
  if (!form.password) return ''
  const hasMinLength = form.password.length >= 8
  const hasLetter = /[A-Za-z]/.test(form.password)
  const hasNumber = /[0-9]/.test(form.password)
  const hasSpecial = /[^A-Za-z0-9]/.test(form.password)

  return hasMinLength && hasLetter && hasNumber && hasSpecial
    ? '사용 가능한 비밀번호입니다.'
    : '8자 이상, 영문+숫자+특수문자 포함해야 합니다.'
})

const isPasswordValid = computed(() =>
  form.password.length >= 8 &&
  /[A-Za-z]/.test(form.password) &&
  /[0-9]/.test(form.password) &&
  /[^A-Za-z0-9]/.test(form.password)
)

const checkUsername = async () => {
  if (!form.username) {
    alertMsg.value = '⚠️ 아이디를 입력해주세요.'
    alertType.value = 'warning'
    return
  }

  try {
    const response = await axios.get(`/api/check-username/?username=${form.username}`)
    usernameStatus.value = response.data.is_taken ? 'taken' : 'available'
  } catch (err) {
    alertMsg.value = '❌ 중복 확인 실패'
    alertType.value = 'danger'
    console.error(err)
  }
}

const sendEmailVerification = async () => {
  if (!form.email) {
    alertMsg.value = '📭 이메일을 입력해주세요.'
    alertType.value = 'warning'
    return
  }

  try {
    const res = await axios.post('/api/send-verification/', {
      email: form.email,
      name: form.name || '',
    })
    localStorage.setItem('pendingSignupData', JSON.stringify(form))
    alertMsg.value = res.data.detail || '📬 인증 메일을 보냈어요. 메일함을 확인해보세요.'
    alertType.value = 'success'
  } catch (err) {
    console.error('❌ 인증 오류:', err)
    alertMsg.value = '❌ 인증 실패: ' + (err.response?.data?.detail || '서버 오류')
    alertType.value = 'danger'
  }
}

onMounted(async () => {
  const uidb64 = route.query.uidb64
  const token = route.query.token
  if (uidb64 && token) {
    const savedForm = JSON.parse(localStorage.getItem('pendingSignupData') || '{}')
    Object.assign(form, savedForm)
    try {
      await axios.post('/api/final-signup/', {
        ...savedForm,
        uidb64,
        token,
        name: savedForm.name || ''  // 👈 name으로 전달
      })
      emailVerified.value = true
      alertMsg.value = '✅ 이메일 인증 완료! 가입 정보를 확인하고 제출해주세요.'
      alertType.value = 'success'
      localStorage.removeItem('pendingSignupData')
    } catch (err) {
      alertMsg.value = '❌ 인증 실패: ' + (err.response?.data?.error || '서버 오류')
      alertType.value = 'danger'
    }
  }
})

const handleSubmit = async () => {
  if (!emailVerified.value) {
    alertMsg.value = '⚠️ 먼저 이메일 인증을 완료해주세요.'
    alertType.value = 'warning'
    return
  }

  if (!isPasswordValid.value) {
    alertMsg.value = '❌ 비밀번호 조건을 확인해주세요.'
    alertType.value = 'danger'
    return
  }

  if (form.password !== form.passwordConfirm) {
    alertMsg.value = '❌ 비밀번호가 일치하지 않습니다.'
    alertType.value = 'danger'
    return
  }
  const birth_date = (form.birthYear && form.birthMonth && form.birthDay)
  ? `${form.birthYear}-${String(form.birthMonth).padStart(2, '0')}-${String(form.birthDay).padStart(2, '0')}`
  : null

  const signupData = {
    name: form.name,
    username: form.username,
    email: form.email,
    password: form.password,
    password_confirm: form.passwordConfirm,
    birth_date: birth_date,
    phone_number: form.phone,
    job: form.job,
  }

  try {
    const res = await axios.post('/api/signup/', signupData)
    if (res.status === 201) {
      alertMsg.value = '🎉 회원가입 성공! 로그인 페이지로 이동합니다.'
      alertType.value = 'success'
      setTimeout(() => router.push('/login'), 2000)
    }
  } catch (err) {
    console.error('회원가입 실패:', err.response?.data || err)
    alertMsg.value = '❌ 회원가입 실패: ' + JSON.stringify(err.response?.data)
    alertType.value = 'danger'
  }
}
</script>


