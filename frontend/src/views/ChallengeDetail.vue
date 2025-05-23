<template>
  <div class="challenge-detail" v-if="challenge">
    <h2>{{ challenge.name }}</h2>
    <p>{{ challenge.description }}</p>
    <hr />

    <div class="plan-info">
      <p>🏦 목표 금액: {{ challenge.goal_amount.toLocaleString() }}원</p>
      <p>⏳ 기간: {{ challenge.total_weeks }}주</p>
      <p>💸 주당 저축: {{ challenge.weekly_saving.toLocaleString() }}원</p>
    </div>

    <div class="calendar-section">
      <h3>📅 저축 달력 (주 단위)</h3>
      <div class="week-calendar">
        <div
          v-for="(week, index) in weeks"
          :key="index"
          :class="['week-cell', { checked: weekChecks[index] }]"
          @click="toggleCheck(index)"
        >
          {{ index + 1 }}주차
        </div>
      </div>
    </div>

    <div class="chart-section">
      <h3>📊 진척도</h3>
      <canvas id="progressChart"></canvas>
    </div>

    <p v-if="isCompleted" class="success">🎉 챌린지를 모두 달성하셨습니다! 멋져요!</p>
    <button @click="endChallenge">챌린지 종료하기</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import { useRoute, useRouter } from 'vue-router'
import { useChallengeStore } from '@/stores/challenge.js'

const store = useChallengeStore()
const route = useRoute()
const router = useRouter()

const challengeData = [
  {
    id: 1,
    name: '비상금 챌린지',
    description: '예상치 못한 상황에 대비한 나만의 비상금 모으기',
    goal_amount: 600000,
    total_weeks: 12,
    weekly_saving: 50000,
  },
  {
    id: 2,
    name: '여행 자금 챌린지',
    description: '버킷리스트 여행을 위해 매주 저축해보세요',
    goal_amount: 1200000,
    total_weeks: 24,
    weekly_saving: 50000,
  },
  {
    id: 3,
    name: '커피 절약 챌린지',
    description: '하루 커피값을 아끼면 한 달에 10만 원 절약!',
    goal_amount: 100000,
    total_weeks: 10,
    weekly_saving: 10000,
  },
  {
    id: 4,
    name: '내 집 마련 챌린지',
    description: '내 집 마련의 첫걸음, 지금부터 차근차근 준비',
    goal_amount: 10000000,
    total_weeks: 100,
    weekly_saving: 100000,
  },
  {
    id: 5,
    name: '결혼 자금 챌린지',
    description: '소중한 날을 위해 계획적인 저축을 시작하세요',
    goal_amount: 5000000,
    total_weeks: 50,
    weekly_saving: 100000,
  },
]

const challenge = ref(null)
const weeks = ref([])
const weekChecks = ref([])
const isCompleted = computed(() => weekChecks.value.every(v => v))

onMounted(() => {
  const id = Number(route.params.id)
  challenge.value = challengeData.find(c => c.id === id)

  if (challenge.value) {
    weeks.value = Array.from({ length: challenge.value.total_weeks })
    weekChecks.value = Array(challenge.value.total_weeks).fill(false)

    // ✅ challenge.value를 사용해 store에 챌린지 등록
    store.startChallenge({
      id: challenge.value.id,
      name: challenge.value.name,
      total_weeks: challenge.value.total_weeks,
    })

    drawChart()
  }
})

const toggleCheck = (index) => {
  weekChecks.value[index] = !weekChecks.value[index]
  if (weekChecks.value[index]) {
    alert(`⭐ ${index + 1}주차 저축 성공! 잘했어요!`)
  }
  drawChart()
}

let chartInstance = null

const drawChart = () => {
  if (!challenge.value) return
  const ctx = document.getElementById('progressChart')
  if (!ctx) return

  if (chartInstance) {
    chartInstance.destroy()
  }

  const saved = weekChecks.value.filter(v => v).length
  const remaining = weekChecks.value.length - saved

  chartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['달성', '남은 기간'],
      datasets: [
        {
          data: [saved, remaining],
          backgroundColor: ['#4caf50', '#e0e0e0'],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
        },
      },
    },
  })
}

const endChallenge = () => {
  if (confirm('정말 종료하시겠습니까?')) {
    store.endChallenge()
    router.push('/saving')
  }
}
</script>


<style scoped>
.challenge-detail {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
}
.plan-info p {
  font-size: 1.1rem;
}
.week-calendar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}
.week-cell {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  text-align: center;
  cursor: pointer;
}
.week-cell.checked {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
}
.chart-section {
  margin-top: 2rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}
.success {
  font-size: 1.2rem;
  margin-top: 1.5rem;
  color: #4caf50;
  text-align: center;
}
</style>
