<template>
  <div class="create-container">
    <h2>🔥 추천 저축 챌린지 중 선택해보세요!</h2>

    <div class="template-recommend">
      <div
        class="template-card"
        v-for="tpl in recommendedTemplates"
        :key="tpl.id"
        :class="{ selected: tpl.id === form.template }"
        @click="selectTemplate(tpl)"
      >
        <h3>{{ tpl.name }}</h3>
        <p>{{ tpl.description }}</p>
      </div>
    </div>

    <hr />

    <label>소득 방식</label>
    <select v-model="incomeType">
      <option value="salary">연봉</option>
      <option value="allowance">용돈</option>
    </select>

    <div v-if="incomeType === 'salary'">
      <input v-model.number="annualSalary" @input="calculateSalary" placeholder="연봉 입력" />
      <p>월 실수령액: {{ monthlySalary }}원</p>
      <input v-model.number="monthlySalary" placeholder="월급 직접 수정 가능" />
    </div>
    <div v-else>
      <input v-model.number="monthlySalary" placeholder="용돈 입력" />
    </div>

    <input v-model="form.goal_amount" placeholder="목표 금액" />
    <input v-model="form.fixed_expenses" placeholder="고정 지출" />
    <input v-model="form.luxury_budget" placeholder="품위유지비" />

    <button @click="submit">챌린지 생성</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const templates = ref([])
const recommendedTemplates = ref([])

const form = ref({
  title: '',
  template: null,
  goal_amount: 0,
  fixed_expenses: 0,
  luxury_budget: 0,
})

const incomeType = ref('salary')
const annualSalary = ref(0)
const monthlySalary = ref(0)

const calculateTax = (income) => {
  const brackets = [
    [0, 14000000, 0.06, 0],
    [14000000, 50000000, 0.15, 840000],
    [50000000, 88000000, 0.24, 6240000],
    [88000000, 150000000, 0.35, 15360000],
    [150000000, 300000000, 0.38, 37060000],
    [300000000, 500000000, 0.40, 94060000],
    [500000000, 1000000000, 0.42, 174060000],
    [1000000000, Infinity, 0.45, 384060000],
  ]
  for (const [lower, upper, rate, base] of brackets) {
    if (income <= upper) return base + (income - lower) * rate
  }
  return 0
}

const calculateSalary = () => {
  const tax = calculateTax(annualSalary.value)
  monthlySalary.value = Math.floor((annualSalary.value - tax) / 12)
}

const selectTemplate = (tpl) => {
  form.value.template = tpl.id
  form.value.title = tpl.name
}

const submit = async () => {
  try {
    await axios.post('/api/savings/challenges/', {
      ...form.value,
      income: monthlySalary.value * 12,
    })
    router.push('/saving')
  } catch (err) {
    console.error('저장 실패:', err.response?.data || err)
  }
}

onMounted(async () => {
  templates.value = [
    { id: 1, name: '비상금 챌린지', description: '예상치 못한 상황에 대비한 나만의 비상금 모으기' },
    { id: 2, name: '여행 자금 챌린지', description: '버킷리스트 여행을 위해 매주 저축해보세요' },
    { id: 3, name: '커피 절약 챌린지', description: '하루 커피값을 아끼면 한 달에 10만 원 절약!' },
    { id: 4, name: '내 집 마련 챌린지', description: '내 집 마련의 첫걸음, 지금부터 차근차근 준비' },
    { id: 5, name: '결혼 자금 챌린지', description: '소중한 날을 위해 계획적인 저축을 시작하세요' },
  ]
  // 랜덤하게 3개 추천
  recommendedTemplates.value = [...templates.value].sort(() => 0.5 - Math.random()).slice(0, 3)
})
</script>

<style scoped>
.create-container {
  max-width: 600px;
  margin: 0 auto;
}
.template-recommend {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.template-card {
  border: 2px solid #ccc;
  border-radius: 10px;
  padding: 1rem;
  flex: 1;
  cursor: pointer;
  transition: 0.3s;
}
.template-card.selected {
  border-color: #4caf50;
  background-color: #f0fff0;
}
</style>
