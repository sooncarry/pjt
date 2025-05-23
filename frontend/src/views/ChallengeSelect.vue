<template>
  <div class="select-page">
    <h2>🔥 원하는 챌린지를 선택해 시작해보세요</h2>
    <div class="template-list">
      <div
        class="template-card"
        v-for="tpl in templates"
        :key="tpl.id"
        @click="goToChallenge(tpl)"
      >
        <h3>{{ tpl.name }}</h3>
        <p>{{ tpl.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const templates = ref([
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
  }
])

const goToChallenge = (tpl) => {
  router.push({
    name: 'ChallengeDetail',
    params: { id: tpl.id },
    state: tpl  // ← Router로 데이터 넘기기 (또는 store에 저장)
  })
}
</script>

<style scoped>
.select-page {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}
.template-list {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}
.template-card {
  border: 2px solid #ddd;
  padding: 1rem;
  width: 200px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;
}
.template-card:hover {
  background-color: #f3f3f3;
}
</style>
