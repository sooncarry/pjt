<template>
  <div class="container my-5">
    <h2 class="h4 fw-bold mb-4">💰 진행 중인 저축 챌린지</h2>

    <div class="d-flex justify-content-end mb-4">
      <button
        class="btn btn-outline-primary btn-sm rounded-pill"
        @click="router.push('/saving/challenges/select')"
      >
        + 챌린지 추가하기
      </button>
    </div>

    <div
      v-for="challenge in challenges"
      :key="challenge.id"
      class="card mb-5 shadow-sm rounded-4 p-4"
    >
      <h4 class="h5 fw-bold mb-2">{{ challenge.template_name }}</h4>
      <p class="text-muted small mb-3">{{ challenge.template_description }}</p>

      <!-- 수정 모드 -->
      <div v-if="editModeMap[challenge.id]" class="mb-3">
        <div class="row g-2 mb-2">
          <div class="col-md-4">
            <label class="form-label small">목표 금액</label>
            <input v-model.number="challenge.goal_amount" type="number" class="form-control form-control-sm" />
          </div>
          <div class="col-md-4">
            <label class="form-label small">기간</label>
            <input v-model.number="challenge.total_units" type="number" class="form-control form-control-sm" />
          </div>
          <div class="col-md-4">
            <label class="form-label small">단위</label>
            <select v-model="challenge.unit" class="form-select form-select-sm">
              <option value="day">일</option>
              <option value="week">주</option>
              <option value="month">월</option>
            </select>
          </div>
        </div>
        <button class="btn btn-success btn-sm rounded-pill mt-2" @click="submitEdit(challenge)">저장</button>
      </div>

      <!-- 일반 정보 -->
      <div v-else class="mb-3">
        <p class="mb-1">🏦 목표 금액: {{ challenge.goal_amount.toLocaleString() }}원</p>
        <p>⏳ 기간: {{ challenge.total_units }} {{ labelUnit(challenge.unit) }}</p>
        <button class="btn btn-outline-secondary btn-sm rounded-pill mt-2" @click="editModeMap[challenge.id] = true">수정하기</button>
      </div>

      <!-- 오늘의 체크 -->
      <div class="mt-4">
        <h5 class="fw-semibold mb-2">✅ 오늘의 저축</h5>
        <button
          class="btn btn-sm rounded-pill"
          :class="challenge.progresses[getCurrentIndex(challenge)]?.is_saved ? 'btn-success' : 'btn-outline-primary'"
          @click="check(challenge.id, getCurrentIndex(challenge))"
          :disabled="!challenge.progresses[getCurrentIndex(challenge)]"
        >
          {{ labelToday(challenge, getCurrentIndex(challenge)) }} 체크
        </button>
      </div>

      <!-- 달력 -->
      <div class="mt-4">
        <h5 class="fw-semibold mb-2">📅 진척도 달력</h5>
        <div class="calendar-grid">
          <div
            v-for="(item, index) in challenge.progresses.slice(0, challenge.total_units)"
            :key="index"
            :class="['calendar-cell', {
              checked: item.is_saved,
              current: index === getCurrentIndex(challenge)
            }]"
          >
            {{ labelCalendar(challenge, index) }}
          </div>
        </div>
      </div>

      <!-- 진행률 -->
      <p class="text-center mt-3 fw-bold">
        🌟 진행률: {{ getSavedCount(challenge) }}/{{ challenge.total_units }} ({{ getProgressPercent(challenge) }}%)
      </p>

      <!-- 종료 버튼 -->
      <div class="text-end mt-3">
        <button class="btn btn-outline-danger btn-sm rounded-pill" @click="endChallenge(challenge.id)">
          챌린지 종료하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const challenges = ref([])
const editModeMap = ref({})

onMounted(async () => {
  const res = await axios.get('/api/savings/active/')
  challenges.value = res.data
  if (challenges.value.length === 0) {
    router.push('/saving')
  }
})

const getSavedCount = (c) => c.progresses.filter(p => p.is_saved).length
const getProgressPercent = (c) => Math.floor(getSavedCount(c) / c.total_units * 100)

const getCurrentIndex = (c) => {
  const start = new Date(c.started_at)
  const today = new Date()
  const diff = today - start
  const oneDay = 1000 * 60 * 60 * 24

  if (c.unit === 'day') {
    return Math.floor(diff / oneDay)
  } else if (c.unit === 'week') {
    return Math.floor(diff / (7 * oneDay))
  } else {
    return (today.getFullYear() - start.getFullYear()) * 12 + (today.getMonth() - start.getMonth())
  }
}

const labelToday = (c, index) => {
  return c.unit === 'day' ? `${index + 1}일차` : c.unit === 'week' ? `${index + 1}주차` : `${index + 1}개월`
}

const labelCalendar = (c, index) => {
  const start = new Date(c.started_at)
  const target = new Date(start)
  if (c.unit === 'day') {
    target.setDate(start.getDate() + index)
    const month = target.getMonth() + 1
    const day = target.getDate()
    return `${month}월 ${day}일`
  } else if (c.unit === 'week') {
    target.setDate(start.getDate() + index * 7)
    const month = target.getMonth() + 1
    const week = Math.ceil((target.getDate() + start.getDay()) / 7)
    return `${month}월 ${week}주차`
  } else {
    target.setMonth(start.getMonth() + index)
    return `${target.getMonth() + 1}월`
  }
}

const labelUnit = (unit) => {
  return unit === 'day' ? '일' : unit === 'week' ? '주' : '개월'
}

const check = async (id, index) => {
  try {
    await axios.post('/api/savings/check/', {
      challenge_id: id,
      unit_index: index
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    const res = await axios.get('/api/savings/active/')
    challenges.value = res.data
  } catch (err) {
    alert('체크 실패')
  }
}

const submitEdit = async (challenge) => {
  try {
    await axios.patch('/api/savings/current/update/', {
      id: challenge.id,
      goal_amount: challenge.goal_amount,
      total_units: challenge.total_units,
      unit: challenge.unit
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    const res = await axios.get('/api/savings/active/')
    challenges.value = res.data
    editModeMap.value[challenge.id] = false
  } catch (err) {
    alert('수정 실패')
  }
}

const endChallenge = async (id) => {
  if (confirm('정말 종료하시겠습니까?')) {
    await axios.post('/api/savings/end/', { id }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    const res = await axios.get('/api/savings/active/')
    challenges.value = res.data
    if (challenges.value.length === 0) {
      router.push('/saving')
    }
  }
}

watch(challenges, (newChallenges) => {
  for (const ch of newChallenges) {
    const saved = ch.progresses.filter(p => p.is_saved).length
    if (saved === ch.total_units) {
      alert(`🎉 '${ch.template_name}' 챌린지를 모두 달성했어요! 수고하셨습니다! 챌린지 기록은 마이페이지에서 확인하실 수 있습니다.`)
      endChallenge(ch.id)
    }
  }
}, { deep: true })
</script>

<style scoped>
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.5rem;
  margin-top: 1rem;
}
.calendar-cell {
  padding: 0.6rem;
  text-align: center;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #f8f9fa;
  font-size: 0.85rem;
}
.calendar-cell.checked {
  background-color: #4caf50;
  color: white;
}
.calendar-cell.current {
  border: 2px solid #2196f3;
  font-weight: bold;
  background-color: #e3f2fd;
}
</style>
