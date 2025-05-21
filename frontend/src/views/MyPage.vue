<template>
  <div class="profile-container">
    <h2>기본 정보</h2>
    <p><strong>아이디</strong>: {{ user.username }}</p>

    <div v-if="isEdit">
      <input v-model="user.birth_date" type="date" />
    </div>
    <div v-else>
      <p>생년월일: {{ user.birth_date }}</p>
    </div>

    <h2>연락처 정보</h2>
    <p><strong>이메일</strong>: {{ user.email }}</p>

    <div v-if="isEdit">
      <input v-model="user.phone_number" type="text" />
    </div>
    <div v-else>
      <p>휴대폰 번호:{{ user.phone_number }}</p>
    </div>

    <div class="button-group">
      <button v-if="!isEdit" @click="isEdit = true">프로필 수정하기</button>
      <button v-else @click="updateProfile">수정 완료</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const user = ref({})
const isEdit = ref(false)

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const res = await axios.get('/accounts/mypage/', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  if (res.data.birth_date) {
    res.data.birth_date = res.data.birth_date.substring(0, 10)
  }
  user.value = res.data
  console.log('마이페이지 응답:', res.data)
})

const updateProfile = async () => {
  const token = localStorage.getItem('access_token')
  await axios.put('/accounts/mypage/', user.value, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  alert('수정되었습니다!')
  isEdit.value = false
}
</script>
