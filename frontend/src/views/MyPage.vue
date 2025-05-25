<template>
  <div class="container my-5">
    <!-- 재무 성향 -->
    <div class="card p-4 mb-4 shadow-sm border-0 rounded-4">
      <h4 class="fw-bold mb-3">📊 나의 재무 성향</h4>
      <div v-if="profileStore.checklistSubmitted">
        <p class="mb-1"><strong>{{ profileStore.title }}</strong></p>
        <p class="text-muted">소비 성향: {{ profileStore.spendingStyle }} / 저축 성향: {{ profileStore.savingStyle }}</p>
      </div>
      <div v-else>
        <router-link to="/checklist" class="btn btn-outline-primary btn-sm rounded-pill">
          📋 나의 재무 성향 체크하러 가기
        </router-link>
      </div>
    </div>

    <!-- 기본 정보 -->
    <div class="card p-4 mb-4 shadow-sm border-0 rounded-4">
      <h4 class="fw-bold mb-3">👤 기본 정보</h4>
      <p><strong>아이디</strong>: {{ user.username }}</p>

      <div v-if="isEdit">
        <label class="form-label small">생년월일</label>
        <input v-model="user.birth_date" type="date" class="form-control form-control-sm mb-2" />
      </div>
      <div v-else>
        <p>생년월일: {{ user.birth_date }}</p>
      </div>

      <h5 class="mt-4 mb-2">📞 연락처 정보</h5>
      <p><strong>이메일</strong>: {{ user.email }}</p>

      <div v-if="isEdit">
        <label class="form-label small">휴대폰 번호</label>
        <input v-model="user.phone_number" type="text" class="form-control form-control-sm mb-2" />
      </div>
      <div v-else>
        <p>휴대폰 번호: {{ user.phone_number }}</p>
      </div>

      <div class="mt-3">
        <button v-if="!isEdit" @click="isEdit = true" class="btn btn-outline-primary btn-sm rounded-pill">
          프로필 수정하기
        </button>
        <button v-else @click="updateProfile" class="btn btn-success btn-sm rounded-pill">
          수정 완료
        </button>
      </div>
    </div>

    <!-- 진행 중인 챌린지 -->
    <div class="card p-4 mb-4 shadow-sm border-0 rounded-4">
      <h4 class="fw-bold mb-3">📌 진행 중인 챌린지</h4>
      <div v-if="activeChallenges.length === 0" class="text-muted">진행 중인 챌린지가 없습니다.</div>
      <div v-else class="row g-3">
        <div
          v-for="ch in activeChallenges"
          :key="ch.id"
          class="col-md-6"
        >
          <div class="border rounded-3 p-3 h-100">
            <h5 class="fw-semibold">{{ ch.template_name }}</h5>
            <p class="text-muted mb-2">{{ ch.goal_amount.toLocaleString() }}원 / {{ ch.total_units }} {{ ch.unit }}</p>
            <button @click="goToDetail()" class="btn btn-outline-success btn-sm rounded-pill">챌린지 보러가기</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 완료된 챌린지 -->
    <div class="card p-4 shadow-sm border-0 rounded-4">
      <h4 class="fw-bold mb-3">🏁 완료된 챌린지</h4>
      <div v-if="completedChallenges.length === 0" class="text-muted">완료된 챌린지가 없습니다.</div>
      <div v-else class="row g-3">
        <div
          v-for="ch in completedChallenges"
          :key="ch.id"
          class="col-md-6"
        >
          <div class="border rounded-3 p-3 bg-light h-100">
            <h5 class="fw-semibold">{{ ch.template_name }}</h5>
            <p class="mb-1">{{ ch.goal_amount.toLocaleString() }}원 / {{ ch.total_units }} {{ ch.unit }}</p>
            <p class="small text-muted">✅ 완료일: {{ ch.completed_at?.slice(0, 10) || '날짜 없음' }}</p>
          </div>
        </div>
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

  const res = await axios.get('/api/mypage/', { headers })
  if (res.data.birth_date) {
    res.data.birth_date = res.data.birth_date.substring(0, 10)
  }
  user.value = res.data

  await profileStore.fetchProfile()

  const res1 = await axios.get('/api/savings/active/', { headers })
  activeChallenges.value = res1.data

  const res2 = await axios.get('/api/savings/history/', { headers })
  completedChallenges.value = res2.data
})

const goToDetail = () => {
  router.push('/saving/challenges')
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

<style scoped>
/* 필요 시만 추가 */
</style>
