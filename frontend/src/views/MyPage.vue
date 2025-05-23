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

  <div class="challenge-section">
    <h2>📌 진행 중인 챌린지</h2>
    <div v-if="activeChallenges.length === 0">진행 중인 챌린지가 없습니다.</div>
    <div v-else class="challenge-list">
      <div
        v-for="ch in activeChallenges"
        :key="ch.id"
        class="challenge-card"
      >
        <h3>{{ ch.template_name }}</h3>
        <p>{{ ch.goal_amount.toLocaleString() }}원 / {{ ch.total_units }} {{ ch.unit }}</p>
        <button @click="goToDetail()">챌린지 보러가기</button>
      </div>
  </div>

  <h2>🏁 완료된 챌린지</h2>
  <div v-if="completedChallenges.length === 0">완료된 챌린지가 없습니다.</div>
    <div v-else class="challenge-list">
      <div
        v-for="ch in completedChallenges"
        :key="ch.id"
        class="challenge-card done"
      >
        <h3>{{ ch.template_name }}</h3>
        <p>{{ ch.goal_amount.toLocaleString() }}원 / {{ ch.total_units }} {{ ch.unit }}</p>
        <p>✅ 완료일: {{ ch.completed_at?.slice(0, 10) || '날짜 없음' }}</p>



      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useProfileStore } from '@/stores/profile'
import { useRouter } from 'vue-router'

const router = useRouter()

const activeChallenges = ref([])
const completedChallenges = ref([])

const user = ref({})
const isEdit = ref(false)

const profileStore = useProfileStore()

onMounted(async () => {
  const token = localStorage.getItem('access_token')
  const headers = {
    Authorization: `Bearer ${token}`
  }

  // 1. 사용자 기본 정보 요청
  const res = await axios.get('/api/mypage/', { headers })
  if (res.data.birth_date) {
    res.data.birth_date = res.data.birth_date.substring(0, 10)
  }
  user.value = res.data

  // 2. 재무 성향 정보 요청
  await profileStore.fetchProfile()

  // 3. 진행 중인 챌린지
  const res1 = await axios.get('/api/savings/active/', { headers })
  activeChallenges.value = res1.data

  // 4. 완료된 챌린지
  const res2 = await axios.get('/api/savings/history/', { headers })
  completedChallenges.value = res2.data
})



const goToDetail = () => {
  router.push('/saving/challenges')  // 현재는 다중 디테일 페이지로 연결
}


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
