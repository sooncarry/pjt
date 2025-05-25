<template>
  <div class="container my-4">
    <h2 class="h5 fw-bold mb-4">📊 현물(주식) 상품 비교</h2>

    <!-- 자동완성 검색창 -->
    <div class="mb-3 position-relative">
      <label class="form-label small">기업명으로 검색</label>
      <input
        v-model="searchInput"
        @input="fetchSuggestions"
        @focus="showSuggestions = true"
        @blur="handleBlur"
        placeholder="예: 삼성전자"
        class="form-control form-control-sm rounded-3"
      />
      <ul
        v-if="showSuggestions && suggestions.length"
        class="list-group position-absolute w-100 mt-1 shadow z-3"
        style="max-height: 200px; overflow-y: auto;"
      >
        <li
          v-for="item in suggestions"
          :key="item.code"
          @mousedown.prevent="selectSuggestion(item)"
          class="list-group-item list-group-item-action small"
          style="cursor: pointer;"
        >
          {{ item.name }} ({{ item.code }})
        </li>
      </ul>
    </div>

    <!-- 종목코드 직접 입력 -->
    <div class="mb-3">
      <label class="form-label small">종목 코드 (쉼표로 구분)</label>
      <input
        v-model="codeInput"
        placeholder="예: 005930,000660"
        class="form-control form-control-sm rounded-3"
      />
    </div>

    <!-- 날짜 선택 -->
    <div class="row g-3 mb-3">
      <div class="col-md-6">
        <label class="form-label small">조회 시작일</label>
        <input v-model="startDate" type="date" class="form-control form-control-sm rounded-3" />
      </div>
      <div class="col-md-6">
        <label class="form-label small">조회 종료일</label>
        <input v-model="endDate" type="date" class="form-control form-control-sm rounded-3" />
      </div>
    </div>

    <!-- 비교 버튼 -->
    <button
      @click="fetchCompareData"
      class="btn btn-primary btn-sm rounded-pill px-4"
    >
      {{ isLoading ? '로딩 중...' : '비교하기' }}
    </button>

    <div v-if="isLoading" class="text-muted mt-3 small">데이터를 불러오는 중입니다...</div>

    <!-- 결과 테이블 -->
    <div v-if="results.length" class="mt-5 table-responsive">
      <h3 class="h6 fw-semibold mb-3">📈 비교 결과</h3>
      <table class="table table-bordered table-sm text-center align-middle">
        <thead class="table-light">
          <tr>
            <th>종목명</th>
            <th>수익률(%)</th>
            <th>평균 거래량</th>
            <th>PER</th>
            <th>PBR</th>
            <th>시가총액</th>
            <th>배당금</th>
            <th>섹터</th>
            <th>산업군</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.code">
            <td>{{ item.name }}</td>
            <td>{{ item.price_change_rate }}</td>
            <td>{{ item.avg_volume.toLocaleString() }}</td>
            <td>{{ item.per ?? '-' }}</td>
            <td>{{ item.pbr ?? '-' }}</td>
            <td>₩{{ formatNumber(item.market_cap) }}</td>
            <td>₩{{ formatNumber(item.dividend.amount) }}</td>
            <td>{{ item.sector }}</td>
            <td>{{ item.industry }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 종가 차트 -->
    <div v-if="results.length" class="mt-5">
      <h3 class="h6 fw-semibold mb-3">📉 가격 차트</h3>
      <canvas ref="chart" class="w-100" style="height: 360px;"></canvas>
    </div>
  </div>
</template>


<script setup>
import { ref, nextTick } from 'vue'
import axios from 'axios'
import {
  Chart,
  registerables
} from 'chart.js'
import 'chartjs-adapter-date-fns'

Chart.register(...registerables)

const searchInput = ref('')
const selectedName = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
const codeInput = ref('')
const startDate = ref('')
const endDate = ref('')
const results = ref([])
const isLoading = ref(false)
const chart = ref(null)
let chartInstance = null

const fetchSuggestions = async () => {
  if (!searchInput.value.trim()) {
    suggestions.value = []
    return
  }
  try {
    const res = await axios.get(`/api/stock/autocomplete/?query=${searchInput.value}`)
    suggestions.value = res.data
  } catch (e) {
    console.error('자동완성 실패', e)
  }
}

const selectSuggestion = (item) => {
  if (!codeInput.value.includes(item.code)) {
    codeInput.value = codeInput.value
      ? `${codeInput.value},${item.code}`
      : item.code
  }
  selectedName.value = item.name
  searchInput.value = item.name
  showSuggestions.value = false
}

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false
  }, 200)
}

const fetchCompareData = async () => {
  let codes = codeInput.value
    .split(',')
    .map(code => code.trim())
    .filter(code => code && code !== '0')

  if (!codes.length) {
    alert('유효한 종목코드를 입력해주세요.')
    return
  }

  isLoading.value = true
  try {
    const res = await axios.post('/api/stock/compare/', {
      codes,
      start_date: startDate.value,
      end_date: endDate.value
    })
    results.value = res.data
    await nextTick()
    drawChart()
  } catch (err) {
    console.error('비교 요청 실패:', err)
    alert('비교 데이터를 불러오는 중 오류가 발생했습니다.')
  } finally {
    isLoading.value = false
  }
}

const drawChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chart.value?.getContext('2d')
  if (!ctx) {
    console.error('⚠️ 차트 컨텍스트 오류')
    return
  }

  const datasets = []

  results.value.forEach(item => {
    const closes = item.history.map(point => point.close)
    const dates = item.history.map(point => point.date)

    const ma5 = closes.map((_, i, arr) => {
      if (i < 4) return null
      const avg = arr.slice(i - 4, i + 1).reduce((a, b) => a + b, 0) / 5
      return avg
    })

    const baseColor = 'rgba(0, 0, 0, 0.3)'
    datasets.push({
      label: item.name,
      data: item.history.map(point => ({ x: point.date, y: point.close })),
      borderWidth: 2,
      fill: false,
      tension: 0.3,
      borderColor: baseColor,
      pointRadius: 2
    })

    datasets.push({
      label: `${item.name} (5일 이동평균)` ,
      data: dates.map((date, i) => ma5[i] ? { x: date, y: ma5[i] } : null).filter(Boolean),
      borderDash: [5, 5],
      borderColor: 'black',
      borderWidth: 2,
      tension: 0.2,
      fill: false,
      pointRadius: 0
    })
  })

  chartInstance = new Chart(ctx, {
    type: 'line',
    data: { datasets },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: '종가 추이 및 5일 이동평균선' }
      },
      scales: {
        x: {
          type: 'time',
          time: { unit: 'day' },
          title: { display: true, text: '날짜' }
        },
        y: {
          title: { display: true, text: '종가 (원)' }
        }
      }
    }
  })
}

function formatNumber(value) {
  if (!value || isNaN(value)) return '-'
  return Number(value).toLocaleString()
}
</script>
