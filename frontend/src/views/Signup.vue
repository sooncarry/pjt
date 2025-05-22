<template>
  <div class="signup">
    <h1>회원가입</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>이름</label>
        <input v-model="form.name" type="text" required />
      </div>

      <div class="form-group username-group">
        <label>아이디</label>
        <input v-model="form.username" type="text" required />
        <button type="button" @click="checkUsername">중복 확인</button>
      </div>
      <p v-if="usernameStatus === 'available'" class="status available">사용 가능한 아이디입니다.</p>
      <p v-else-if="usernameStatus === 'taken'" class="status taken">이미 사용 중인 아이디입니다.</p>

      <div class="form-group">
        <label>비밀번호</label>
        <input v-model="form.password" type="password" required />
        <!-- ★ 비밀번호 조건 메시지 -->
        <p class="password-check" :class="{ valid: isPasswordValid, invalid: !isPasswordValid && form.password }">
          {{ passwordMessage }}
        </p>
      </div>

      <div class="form-group">
        <label>비밀번호 확인</label>
        <input v-model="form.passwordConfirm" type="password" required />
      </div>

      <div class="form-group email-group">
        <label>이메일</label>
        <input v-model="form.email" type="email" required />
        <button type="button" @click="sendEmailVerification">인증</button>
      </div>

      <div class="form-group">
        <label>생년월일</label>
        <div class="birth-select">
          <select v-model="form.birthYear" required>
            <option disabled value="">년도</option>
            <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
          </select>
          <select v-model="form.birthMonth" required>
            <option disabled value="">월</option>
            <option v-for="month in 12" :key="month" :value="month">{{ month }}</option>
          </select>
          <select v-model="form.birthDay" required>
            <option disabled value="">일</option>
            <option v-for="day in 31" :key="day" :value="day">{{ day }}</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label>전화번호</label>
        <input v-model="form.phone" type="tel" />
      </div>

      <div class="form-group">
        <label>주소</label>
        <input v-model="form.address" type="text" />
      </div>

      <div class="form-group">
        <label>직업</label>
        <select v-model="form.job">
          <option disabled value="">선택하세요</option>
          <option>학생</option>
          <option>회사원</option>
          <option>프리랜서</option>
          <option>무직</option>
          <option>기타</option>
        </select>
      </div>

      <div class="form-group">
        <label>금융 성향</label>
        <div class="radio-group">
          <label><input type="radio" value="보수적" v-model="form.riskType" /> 보수적</label>
          <label><input type="radio" value="중립적" v-model="form.riskType" /> 중립적</label>
          <label><input type="radio" value="공격적" v-model="form.riskType" /> 공격적</label>
        </div>
      </div>

      <button type="submit">가입하기</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import axios from 'axios'

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
  address: '',
  job: '',
  riskType: '',
})

const usernameStatus = ref('') // '', 'available', 'taken'

// ★ 비밀번호 유효성 검사
const passwordMessage = computed(() => {
  if (!form.password) return ''
  const hasMinLength = form.password.length >= 8
  const hasLetter = /[A-Za-z]/.test(form.password)
  const hasNumber = /[0-9]/.test(form.password)
  const hasSpecial = /[^A-Za-z0-9]/.test(form.password)

  if (hasMinLength && hasLetter && hasNumber && hasSpecial) {
    return '사용 가능한 비밀번호입니다.'
  } else {
    return '8자 이상, 영문+숫자+특수문자 포함해야 합니다.'
  }
})

const isPasswordValid = computed(() =>
  form.password.length >= 8 &&
  /[A-Za-z]/.test(form.password) &&
  /[0-9]/.test(form.password) &&
  /[^A-Za-z0-9]/.test(form.password)
)

const checkUsername = async () => {
  if (!form.username) {
    alert('아이디를 입력해주세요.')
    return
  }

  try {
    const response = await axios.get(`/api/check-username/?username=${form.username}`)
    usernameStatus.value = response.data.is_taken ? 'taken' : 'available'
  } catch (err) {
    alert('중복 확인 실패')
    console.error(err)
  }
}

const sendEmailVerification = () => {
  alert('이메일 인증 전송 기능은 추후 구현 예정입니다.')
}

import { useRouter } from 'vue-router'
const router = useRouter()

const handleSubmit = async () => {
  if (!isPasswordValid.value) {
    alert('비밀번호 조건을 확인해주세요.')
    return
  }

  if (form.password !== form.passwordConfirm) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  const signupData = {
    username: form.username,
    email: form.email,
    password: form.password,
    password_confirm: form.passwordConfirm,
    first_name: form.name,
    birth_date: `${form.birthYear}-${String(form.birthMonth).padStart(2, '0')}-${String(form.birthDay).padStart(2, '0')}`,
    phone_number: form.phone,
    address: form.address,
    job: form.job,
    risk_type: form.riskType
  }

  try {
    const res = await axios.post('/api/signup/', signupData)
    if (res.status === 201) {
      alert('회원가입 성공!')
      router.push('/login')  
    }
  } catch (err) {
    console.error('회원가입 실패:', err.response?.data || err)
    alert('회원가입 실패: ' + JSON.stringify(err.response?.data))
  }
}

</script>

<style scoped>
.signup {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.email-group,
.username-group {
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

input,
select,
button {
  padding: 0.5rem;
  font-size: 1rem;
}

.birth-select {
  display: flex;
  gap: 0.5rem;
}

.radio-group {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.status {
  font-size: 0.9rem;
}
.status.available {
  color: green;
}
.status.taken {
  color: red;
}

.password-check {
  font-size: 0.85rem;
  margin-top: 0.25rem;
}
.password-check.valid {
  color: green;
}
.password-check.invalid {
  color: red;
}

button[type="submit"] {
  margin-top: 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}
button[type="submit"]:hover {
  background-color: #0056b3;
}
</style>
