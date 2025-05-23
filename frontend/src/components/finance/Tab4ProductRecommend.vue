<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">맞춤형 상품 추천</h2>

    <!-- 입력 방식 선택 -->
    <div class="mb-4">
      <label><input type="radio" value="salary" v-model="inputType" /> 연봉 기준</label>
      <label class="ml-4"><input type="radio" value="allowance" v-model="inputType" /> 월 용돈 입력</label>
    </div>

    <!-- 연봉 or 용돈 입력 -->
    <div v-if="inputType === 'salary'" class="mb-2">
      <input v-model.number="yearlyIncome" type="number" placeholder="연봉 입력 (원)" class="input" />
      <p class="text-sm text-gray-500 mt-1">실수령 월급: {{ monthlyIncome.toLocaleString() }}원</p>
    </div>
    <div v-else class="mb-2">
      <input v-model.number="manualInput" type="number" placeholder="월 용돈 입력 (원)" class="input" />
    </div>

    <!-- 상품 유형 선택 -->
    <div class="mb-2">
      <label><input type="radio" value="all" v-model="productType" /> 전체</label>
      <label class="ml-4"><input type="radio" value="deposit" v-model="productType" /> 예금</label>
      <label class="ml-4"><input type="radio" value="saving" v-model="productType" /> 적금</label>
    </div>

    <!-- 가입 기간 선택 -->
    <div class="mb-4">
      <label for="term">가입 기간 (개월):</label>
      <select id="term" v-model="term" class="input ml-2">
        <option value="">전체</option>
        <option value="6">6개월</option>
        <option value="12">12개월</option>
        <option value="24">24개월</option>
        <option value="36">36개월</option>
      </select>
    </div>

    <!-- 추천 버튼 -->
    <button @click="fetchRecommendations" class="btn">추천 받기</button>

    <!-- 추천 결과 -->
    <div v-if="recommendations.length" class="mt-6">
      <h3 class="font-semibold mb-2">📌 추천 상품</h3>
      <ul>
        <li v-for="product in recommendations" :key="product.id" class="mb-1">
          <strong>{{ product.name }}</strong><br />
          - 상품 유형: {{ product.type === 'saving' ? '적금' : '예금' }}<br />
          - 금리: {{ product.interest_rate }}%<br />
          - 가입 기간: {{ product.term }}개월<br />
          <span v-if="product.etc_note">📝 {{ product.etc_note }}</span>
        </li>
      </ul>
    </div>
    <div v-else-if="fetched" class="mt-4 text-red-500">
      추천 가능한 상품이 없습니다 😥
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const inputType = ref('salary')
const yearlyIncome = ref(40000000)
const manualInput = ref(300000)
const productType = ref('all')
const term = ref('')
const recommendations = ref([])
const fetched = ref(false)

const monthlyIncome = computed(() =>
  inputType.value === 'salary'
    ? Math.round((yearlyIncome.value - calculateTax(yearlyIncome.value)) / 12)
    : manualInput.value
)

const fetchRecommendations = async () => {
  fetched.value = false
  try {
    // 1. 사용자 프로필 체크
    const profileRes = await axios.get('http://localhost:8000/api/finance/check-profile/')
    if (!profileRes.data.has_profile) {
      alert('재무 성향 체크가 필요합니다. 마이페이지로 이동합니다.')
      router.push('/mypage')
      return
    }

    // 2. 추천 상품 호출
    const params = new URLSearchParams({
      monthly_income: monthlyIncome.value,
      type: productType.value,
    })
    if (term.value) params.append('term', term.value)

    const { data } = await axios.get(`http://localhost:8000/api/finance/recommend-products/?${params}`)
    recommendations.value = data
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert('로그인이 필요합니다. 로그인 페이지로 이동합니다.')
      router.push('/signin')
    } else {
      console.error('추천 API 호출 실패:', error)
      recommendations.value = []
    }
  } finally {
    fetched.value = true
  }
}

function calculateTax(income) {
  if (income <= 14000000) return income * 0.06;
  else if (income <= 50000000) return 840000 + (income - 14000000) * 0.15;
  else if (income <= 88000000) return 6240000 + (income - 50000000) * 0.24;
  else if (income <= 150000000) return 15360000 + (income - 88000000) * 0.35;
  else if (income <= 300000000) return 37060000 + (income - 150000000) * 0.38;
  else if (income <= 500000000) return 94060000 + (income - 300000000) * 0.40;
  else if (income <= 1000000000) return 174060000 + (income - 500000000) * 0.42;
  else return 384060000 + (income - 1000000000) * 0.45;
}
</script>

<style scoped>
.input {
  border: 1px solid #ccc;
  padding: 4px 8px;
}
.btn {
  background-color: #2563eb;
  color: white;
  padding: 6px 14px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
