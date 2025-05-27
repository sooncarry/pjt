<template>
  <div class="container my-5" style="padding-top: 120px;">
    <h2 class="h4 fw-bold mb-4">💰 진행 중인 저축 챌린지</h2>

    <!-- 챌린지 추가 버튼 -->
    <div class="d-flex justify-content-end mb-4">
      <button class="btn btn-outline-primary btn-sm rounded-pill"
              @click="router.push('/saving/challenges/select')">
        + 챌린지 추가하기
      </button>
    </div>

    <!-- 챌린지 카드 -->
    <div v-for="challenge in challenges"
         :key="challenge.id"
         class="card mb-5 shadow-sm rounded-4 p-4">

      <!-- 제목·설명 -->
      <h4 class="h5 fw-bold mb-2">{{ challenge.template_name }}</h4>
      <p class="text-muted small mb-3">{{ challenge.template_description }}</p>

      <!-- ▸ 편집 모드 ------------------------------ -->
      <div v-if="editModeMap[challenge.id]" class="mb-3">
        <div class="row g-2 mb-2">
          <div class="col-md-4">
            <label class="form-label small">목표 금액</label>
            <input v-model.number="challenge.goal_amount"
                   type="number"
                   class="form-control form-control-sm" />
          </div>
          <div class="col-md-4">
            <label class="form-label small">기간</label>
            <input v-model.number="challenge.total_units"
                   type="number"
                   class="form-control form-control-sm" />
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
        <button class="btn btn-success btn-sm rounded-pill mt-2"
                @click="submitEdit(challenge)">
          저장
        </button>
      </div>

      <!-- ▸ 일반 정보 ------------------------------ -->
      <div v-else class="mb-3">
        <p class="mb-1">🏦 목표 금액: {{ challenge.goal_amount.toLocaleString() }}원</p>
        <p>⏳ 기간: {{ challenge.total_units }} {{ labelUnit(challenge.unit) }}</p>
        <button class="btn btn-outline-secondary btn-sm rounded-pill mt-2"
                @click="editModeMap[challenge.id] = true">
          수정하기
        </button>
      </div>

      <!-- ▸ 오늘 체크 버튼 ------------------------ -->
      <div class="mt-4">
        <h5 class="fw-semibold mb-2">✅ 오늘의 저축</h5>
        <button class="btn btn-sm rounded-pill"
                :class="challenge.progresses[getCurrentIndex(challenge)]?.is_saved
                        ? 'btn-success' : 'btn-outline-primary'"
                @click="check(challenge.id, getCurrentIndex(challenge))"
                :disabled="!challenge.progresses[getCurrentIndex(challenge)]">
          {{ labelToday(challenge, getCurrentIndex(challenge)) }} 체크
        </button>
      </div>

      <!-- ▸ 달력 ------------------------------ -->
      <div class="mt-4">
        <h5 class="fw-semibold mb-2">📅 진척도 달력</h5>
        <div class="calendar-grid">
          <div v-for="(item, idx) in challenge.progresses.slice(0, challenge.total_units)"
               :key="idx"
               :class="['calendar-cell', {
                 checked: item.is_saved,
                 current: idx === getCurrentIndex(challenge)
               }]">
            {{ labelCalendar(challenge, idx) }}
          </div>
        </div>
      </div>

      <!-- ▸ 진행률 ------------------------------ -->
      <p class="text-center mt-3 fw-bold">
        🌟 진행률: {{ getSavedCount(challenge) }}/{{ challenge.total_units }}
        ({{ getProgressPercent(challenge) }}%)
      </p>

      <!-- ▸ 포기 버튼 ---------------------------- -->
      <div class="text-end mt-3">
        <button class="btn btn-outline-danger btn-sm rounded-pill"
                @click="endChallenge(challenge.id, false)">
          챌린지 포기하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router       = useRouter()
const challenges   = ref([])
const editModeMap  = ref({})

/* -------------------------------------------------- */
/* 공통 헤더 */
const authHeader = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` }
})

/* -------------------------------------------------- */
/* 초기 로드 */
onMounted(loadActiveChallenges)

async function loadActiveChallenges () {
  const { data } = await axios.get('/api/savings/active/', authHeader())
  challenges.value = data
  if (!data.length) router.push('/saving')
}

/* -------------------------------------------------- */
/* 헬퍼 함수들 */
const getSavedCount      = c => c.progresses.filter(p => p.is_saved).length
const getProgressPercent = c => Math.floor(getSavedCount(c) / c.total_units * 100)
const labelUnit          = u => u === 'day' ? '일' : u === 'week' ? '주' : '개월'

const getCurrentIndex = c => {
  const start = new Date(c.started_at)
  const today = new Date()
  const diff  = today - start
  const D     = 86_400_000
  if (c.unit === 'day')   return Math.floor(diff / D)
  if (c.unit === 'week')  return Math.floor(diff / (7 * D))
  /* month */             return (today.getFullYear() - start.getFullYear()) * 12
                               + (today.getMonth() - start.getMonth())
}

const labelToday = (c, idx) =>
  c.unit === 'day'  ? `${idx + 1}일차`
  : c.unit === 'week' ? `${idx + 1}주차`
  : `${idx + 1}개월`

const labelCalendar = (c, idx) => {
  const start  = new Date(c.started_at)
  const target = new Date(start)
  if (c.unit === 'day') {
    target.setDate(start.getDate() + idx)
    return `${target.getMonth() + 1}월 ${target.getDate()}일`
  }
  if (c.unit === 'week') {
    target.setDate(start.getDate() + idx * 7)
    const week = Math.ceil((target.getDate() + start.getDay()) / 7)
    return `${target.getMonth() + 1}월 ${week}주차`
  }
  target.setMonth(start.getMonth() + idx)
  return `${target.getMonth() + 1}월`
}

/* -------------------------------------------------- */
/* 체크 토글 */
async function check (id, idx) {
  try {
    await axios.post('/api/savings/check/',
      { challenge_id: id, unit_index: idx },
      authHeader())
    await loadActiveChallenges()
  } catch { alert('체크 실패') }
}

/* -------------------------------------------------- */
/* 편집 저장 */
async function submitEdit (c) {
  try {
    await axios.patch('/api/savings/current/update/',
      {
        id          : c.id,
        goal_amount : c.goal_amount,
        total_units : c.total_units,
        unit        : c.unit
      },
      authHeader())
    await loadActiveChallenges()
    editModeMap.value[c.id] = false
  } catch { alert('수정 실패') }
}

/* -------------------------------------------------- */
/* 종료 처리 (success = true 완료 / false 포기) */
async function endChallenge (id, success = false) {
  const ok = success || confirm('정말 포기하시겠습니까?')
  if (!ok) return
  try {
    await axios.post('/api/savings/end/', { id, success }, authHeader())
    await loadActiveChallenges()
  } catch { alert('처리 실패') }
}

/* -------------------------------------------------- */
/* 진행률 100% 감지 → 완료 처리 */
watch(challenges, list => {
  list.forEach(c => {
    if (getSavedCount(c) === c.total_units) {
      alert(`🎉 '${c.template_name}' 챌린지를 모두 달성했어요!`)
      endChallenge(c.id, true)
    }
  })
}, { deep: true })
</script>

<style scoped>
.calendar-grid  { display:grid; grid-template-columns:repeat(4,1fr);
                  gap:.5rem; margin-top:1rem; }
.calendar-cell  { padding:.6rem; text-align:center; border-radius:6px;
                  border:1px solid #ccc; background:#f8f9fa; font-size:.85rem; }
.calendar-cell.checked { background:#4caf50; color:#fff; }
.calendar-cell.current { border:2px solid #2196f3; font-weight:bold;
                         background:#e3f2fd; }
</style>
