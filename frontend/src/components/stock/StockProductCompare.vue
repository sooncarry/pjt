<template>
  <div class="p-4 relative">
    <h2 class="text-xl font-bold mb-4">📊 현물(주식) 상품 비교</h2>

    <!-- 자동완성 검색창 -->
    <div class="mb-4 relative">
      <label class="block text-sm font-medium mb-1">기업명으로 검색</label>
      <input
        v-model="searchInput"
        @input="fetchSuggestions"
        @focus="showSuggestions = true"
        @blur="hideSuggestions"
        placeholder="예: 삼성전자"
        class="w-full border px-3 py-2 rounded"
      />
      <!-- 자동완성 드롭다운 -->
      <ul v-if="showSuggestions && suggestions.length" class="absolute z-10 bg-white border rounded mt-1 shadow w-full max-h-48 overflow-auto">
        <li
          v-for="item in suggestions"
          :key="item.code"
          @mousedown.prevent="selectSuggestion(item)"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
        >
          {{ item.name }} <span v-if="item.code">({{ item.code }})</span>
        </li>
      </ul>
    </div>

    <!-- 종목코드 직접 입력 -->
    <div class="mb-4">
      <label class="block text-sm font-medium mb-1">종목 코드 (쉼표로 구분)</label>
      <input v-model="codeInput" type="text" placeholder="예: 005930,000660"
        class="w-full border px-3 py-2 rounded" />
    </div>

    <!-- 날짜 선택 -->
    <div class="mb-4 flex gap-4">
      <div>
        <label class="block text-sm font-medium mb-1">조회 시작일</label>
        <input v-model="startDate" type="date" class="border px-2 py-1 rounded" />
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">조회 종료일</label>
        <input v-model="endDate" type="date" class="border px-2 py-1 rounded" />
      </div>
    </div>

    <!-- 비교 버튼 -->
    <button @click="fetchCompareData"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
      비교하기
    </button>

    <!-- 결과 테이블 -->
    <div v-if="results.length" class="mt-6 overflow-x-auto">
      <h3 class="text-lg font-semibold mb-2">📈 비교 결과</h3>
      <table class="w-full text-sm border">
        <thead class="bg-gray-100">
          <tr>
            <th class="border px-2 py-1">종목명</th>
            <th class="border px-2 py-1">수익률(%)</th>
            <th class="border px-2 py-1">평균 거래량</th>
            <th class="border px-2 py-1">PER</th>
            <th class="border px-2 py-1">PBR</th>
            <th class="border px-2 py-1">시가총액</th>
            <th class="border px-2 py-1">배당금</th>
            <th class="border px-2 py-1">배당수익률(%)</th>
            <th class="border px-2 py-1">섹터</th>
            <th class="border px-2 py-1">산업군</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.code">
            <td class="border px-2 py-1">{{ item.name }}</td>
            <td class="border px-2 py-1">{{ item.price_change_rate }}</td>
            <td class="border px-2 py-1">{{ item.avg_volume.toLocaleString() }}</td>
            <td class="border px-2 py-1">{{ item.per ?? '-' }}</td>
            <td class="border px-2 py-1">{{ item.pbr ?? '-' }}</td>
            <td class="border px-2 py-1">{{ item.market_cap?.toLocaleString() ?? '-' }}</td>
            <td class="border px-2 py-1">{{ item.dividend.amount }}</td>
            <td class="border px-2 py-1">{{ item.dividend.yield }}</td>
            <td class="border px-2 py-1">{{ item.sector }}</td>
            <td class="border px-2 py-1">{{ item.industry }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 종가 차트 -->
    <div v-if="results.length" class="mt-10">
      <h3 class="text-lg font-semibold mb-2">📉 가격 차트</h3>
      <canvas ref="chart" class="max-w-full"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import {
  Chart, registerables
} from 'chart.js'

Chart.register(...registerables)

const searchInput = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)

const codeInput = ref('')
const startDate = ref('')
const endDate = ref('')
const results = ref([])
const chart = ref(null)
let chartInstance = null

const fetchSuggestions = async () => {
  if (!searchInput.value.trim()) {
    suggestions.value = []
    return
  }
  try {
    const res = await axios.get(`/api/stock/autocomplete?query=${searchInput.value}`)
    suggestions.value = res.data
  } catch (e) {
    console.error('자동완성 실패', e)
  }
}

const selectSuggestion = (item) => {
  if (!item.code || item.code === '0') return  // 코드 없는 항목 제외
  const code = item.code.padStart(6, '0')      // 안전하게 6자리 보장

  if (!codeInput.value.includes(code)) {
    codeInput.value = codeInput.value
      ? `${codeInput.value},${code}`
      : code
  }

  searchInput.value = ''
  suggestions.value = []
  showSuggestions.value = false
}

const hideSuggestions = () => {
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

const fetchCompareData = async () => {
  let codes = codeInput.value
    .split(',')
    .map(code => code.trim())
    .filter(code => /^[0-9]{6}$/.test(code))  // 정확히 6자리 숫자만 허용

  if (!codes.length) {
    alert('유효한 종목코드를 입력해주세요.')
    return
  }

  try {
    const res = await axios.post('/api/stock/compare/', {
      codes,
      start_date: startDate.value,
      end_date: endDate.value
    })
    results.value = res.data
    drawChart()
  } catch (err) {
    console.error('비교 요청 실패:', err)
    alert('비교 데이터를 불러오는 중 오류가 발생했습니다.')
  }
}

const drawChart = () => {
  console.log('📉 전체 비교 결과:', results.value)
  console.log('📉 첫 종목의 history:', results.value[0]?.history)
  if (chartInstance) chartInstance.destroy()

  const datasets = results.value.map(item => ({
    label: item.name,
    data: item.history.map(point => point.close),
    borderWidth: 2,
    fill: false,
    tension: 0.3
  }))

  const labels = results.value[0]?.history.map(point => point.date) || []

  chartInstance = new Chart(chart.value, {
    type: 'line',
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: {
          display: true,
          text: '종가 추이'
        }
      },
      scales: {
        x: {
          title: { display: true, text: '날짜' },
          ticks: { maxRotation: 90, minRotation: 45 }
        },
        y: {
          title: { display: true, text: '종가 (원)' }
        }
      }
    }
  })
}

</script>
