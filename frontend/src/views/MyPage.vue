<template>
  <div>
    <div v-if="profileStore.checklistSubmitted">
      <h2>{{ profileStore.title }}</h2>
      <p>소비 성향: {{ profileStore.spendingStyle }} / 저축 성향: {{ profileStore.savingStyle }}</p>
    </div>
    <div v-else>
      <router-link to="/checklist">📋 나의 재무 성향 체크하러 가기</router-link>
    </div>
  </div>
  <div class="profile-container">
    <h2>기본 정보</h2>
    <p><strong>아이디</strong>: {{ user.username }}</p>

    <div v-if="isEdit">
      <label for="">생년월일 : </label>
      <input v-model="user.birth_date" type="date" />
    </div>
    <div v-else>
      <p>생년월일: {{ user.birth_date }}</p>
    </div>

    <h2>연락처 정보</h2>
    <p><strong>이메일</strong>: {{ user.email }}</p>

    <div v-if="isEdit">
      <label for="">휴대폰 번호 : </label>
      <input v-model="user.phone_number" type="text"/>
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
import { useProfileStore } from '@/stores/profile'

const user = ref({})
const isEdit = ref(false)

const profileStore = useProfileStore()

onMounted(async () => {
  const token = localStorage.getItem('access_token')

  // 1. 사용자 기본 정보 요청
  const res = await axios.get('/api/mypage/', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  if (res.data.birth_date) {
    res.data.birth_date = res.data.birth_date.substring(0, 10)
  }
  user.value = res.data

  // 2. 재무 성향 정보 요청
  await profileStore.fetchProfile()
})

const updateProfile = async () => {
  const token = localStorage.getItem('access_token')
  await axios.put('/api/mypage/', user.value, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  alert('수정되었습니다!')
  isEdit.value = false
}
</script>
