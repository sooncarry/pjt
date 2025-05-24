<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">맞춤형 상품 추천</h2>

    <!-- 입력 방식 선택 -->
    <div class="mb-4">
      <label><input type="radio" value="salary" v-model="inputType" /> 연봉 기준</label>
      <label class="ml-4"><input type="radio" value="allowance" v-model="inputType" /> 월 용돈 입력</label>
    </div>

    <!-- 연봉 입력 및 실수령 월급 -->
    <div v-if="inputType === 'salary'" class="mb-2">
      <input
        v-model="formattedSalary"
        type="text"
        :placeholder="salaryPlaceholder"
        class="input"
        @input="onSalaryInput"
      />
      <div class="mt-1">
        <template v-if="!editMode">
          <p class="text-sm text-gray-500">
            실수령 월급: {{ formattedMonthlyIncome }}원
            <button @click="editMode = true" class="ml-2 text-blue-600 underline text-xs">직접 입력하기</button>
          </p>
        </template>
        <template v-else>
          <input
            v-model="formattedCustomIncome"
            type="text"
            placeholder="실수령 월급을 직접 입력해주세요"
            class="input mt-1"
            @input="onCustomIncomeInput"
          />
          <button @click="editMode = false" class="text-blue-600 underline text-xs mt-1">← 자동 계산으로 전환</button>
        </template>
      </div>
    </div>

    <!-- 월 용돈 입력 -->
    <div v-if="inputType === 'allowance'" class="mb-2">
      <input
        v-model="formattedManualInput"
        type="text"
        :placeholder="allowancePlaceholder"
        class="input"
        @input="onManualInput"
      />
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
const yearlyIncome = ref(null)
const manualInput = ref(null)
const customIncome = ref(null)
const editMode = ref(false)
const productType = ref('all')
const term = ref('')
const recommendations = ref([])
const fetched = ref(false)

const salaryPlaceholder = computed(() => '연봉을 입력해주세요')
const allowancePlaceholder = computed(() => '매달 사용하는 용돈을 입력해주세요')

const monthlyIncome = computed(() => {
  if (inputType.value === 'salary') {
    if (editMode.value && customIncome.value !== null) {
      return parseInt(String(customIncome.value).replace(/,/g, '')) || 0
    } else if (yearlyIncome.value) {
      return Math.round((yearlyIncome.value - calculateTax(yearlyIncome.value)) / 12)
    }
    return 0
  } else {
    return manualInput.value || 0
  }
})

const formatNumber = (val) => val ? String(val).replace(/\B(?=(\d{3})+(?!\d))/g, ",") : ''

const formattedSalary = computed({
  get: () => formatNumber(yearlyIncome.value),
  set: (val) => { yearlyIncome.value = parseInt(val.replace(/,/g, '')) || null }
})

const formattedCustomIncome = computed({
  get: () => formatNumber(customIncome.value),
  set: (val) => { customIncome.value = parseInt(val.replace(/,/g, '')) || null }
})

const formattedManualInput = computed({
  get: () => formatNumber(manualInput.value),
  set: (val) => { manualInput.value = parseInt(val.replace(/,/g, '')) || null }
})

const formattedMonthlyIncome = computed(() => formatNumber(monthlyIncome.value))

const onSalaryInput = () => {}
const onCustomIncomeInput = () => {}
const onManualInput = () => {}

const fetchRecommendations = async () => {
  fetched.value = false
  try {
    const profileRes = await axios.get('http://localhost:8000/api/finance/check-profile/')
    if (!profileRes.data.has_profile) {
      alert('재무 성향 체크가 필요합니다. 마이페이지로 이동합니다.')
      router.push('/mypage')
      return
    }

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
  width: 100%;
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
