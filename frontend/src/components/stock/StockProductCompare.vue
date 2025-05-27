<!-- StockProductCompare.vue -->
<template>
  <div class="container my-4">
    <h2 class="h5 fw-bold mb-4">📊 현물(주식) 상품 비교</h2>

    <!-- ───── 검색 영역 ───── -->
    <div class="mb-3 position-relative">
      <label class="form-label small">기업명으로 검색</label>
      <input v-model="searchInput" @input="fetchSuggestions"
             @focus="showSuggestions = true" @blur="handleBlur"
             placeholder="예: 삼성전자"
             class="form-control form-control-sm rounded-3" />
      <ul v-if="showSuggestions && suggestions.length"
          class="list-group position-absolute w-100 mt-1 shadow z-3"
          style="max-height:200px;overflow-y:auto">
        <li v-for="item in suggestions" :key="item.code"
            @mousedown.prevent="selectSuggestion(item)"
            class="list-group-item list-group-item-action small"
            style="cursor:pointer">
          {{ item.name }} ({{ item.code }})
        </li>
      </ul>
    </div>

    <!-- 종목 코드 입력 -->
    <div class="mb-3">
      <label class="form-label small">종목 코드</label>
      <input v-model="codeInput"
             placeholder="예: 005930"
             class="form-control form-control-sm rounded-3" />
    </div>

    <!-- 날짜 선택 -->
    <div class="row g-3 mb-3">
      <div class="col-md-6">
        <label class="form-label small">조회 시작일</label>
        <input v-model="startDate" type="date"
               class="form-control form-control-sm rounded-3" />
      </div>
      <div class="col-md-6">
        <label class="form-label small">조회 종료일</label>
        <input v-model="endDate" type="date"
               class="form-control form-control-sm rounded-3" />
      </div>
    </div>

    <button @click="fetchCompareData"
            class="btn btn-primary btn-sm rounded-pill px-4">
      {{ isLoading ? '로딩 중...' : '비교하기' }}
    </button>
    <div v-if="isLoading" class="text-muted mt-3 small">
      데이터를 불러오는 중입니다...
    </div>

    <!-- ───── 결과 테이블 ───── -->
    <div v-if="results.length" class="mt-5 table-responsive">
      <h3 class="h6 fw-semibold mb-3">📈 비교 결과</h3>
      <table class="table table-bordered table-sm text-center align-middle">
        <thead class="table-light">
          <tr>
            <th>종목명</th><th>기간 수익률 (%)</th>
            <th>변동성 (%)</th><th>최대 낙폭 (%)</th><th>평균 거래량</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in results" :key="item.code">
            <td>{{ item.name }}</td>
            <td>{{ item.ret.toFixed(2) }}</td>
            <td>{{ item.vol.toFixed(2) }}</td>
            <td>{{ item.mdd.toFixed(2) }}</td>
            <td>{{ item.avg_volume.toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ───── 차트 영역 ───── -->
    <div v-if="results.length" class="mt-5">
      <ul class="nav nav-tabs mb-3">
        <li class="nav-item">
          <button class="nav-link"
                  :class="{active: chartMode==='line'}"
                  @click="switchChart('line')">라인 & 이동평균</button>
        </li>
        <li class="nav-item">
          <button class="nav-link"
                  :class="{active: chartMode==='candle'}"
                  @click="switchChart('candle')">캔들스틱 & 거래량</button>
        </li>
      </ul>

      <!-- 라인 + 이동평균 -->
      <div v-show="chartMode==='line'"
           class="chart-box position-relative w-100" style="height:380px">
        <canvas ref="lineCanvas"
                class="position-absolute start-0 top-0 w-100 h-100"></canvas>
      </div>

      <!-- 캔들 + 거래량 -->
      <div v-show="chartMode==='candle'">
        <div class="chart-box position-relative w-100" style="height:300px">
          <canvas ref="candleCanvas"
                  class="position-absolute start-0 top-0 w-100 h-100"></canvas>
        </div>
        <div class="chart-box position-relative w-100 mt-2" style="height:120px">
          <canvas ref="volumeCanvas"
                  class="position-absolute start-0 top-0 w-100 h-100"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* ───────── 의존성 ───────── */
import { ref, nextTick } from 'vue'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'
import {
  CandlestickController, CandlestickElement,
  OhlcController,       OhlcElement
} from 'chartjs-chart-financial'
import 'chartjs-adapter-date-fns'

Chart.register(
  ...registerables,
  CandlestickController, CandlestickElement,
  OhlcController,        OhlcElement
)

/* ───────── 상태 ───────── */
const searchInput = ref(''); const suggestions = ref([])
const showSuggestions = ref(false)
const codeInput = ref('')
const startDate = ref(''); const endDate = ref('')
const results = ref([]);  const isLoading = ref(false)

const lineCanvas = ref(null), candleCanvas = ref(null), volumeCanvas = ref(null)
let lineChart = null, candleChart = null, volumeChart = null
const chartMode = ref('line')

/* ───────── 자동완성 ───────── */
async function fetchSuggestions () {
  if (!searchInput.value.trim()) return suggestions.value = []
  try {
    const { data } = await axios.get(`/api/stock/autocomplete/?query=${searchInput.value}`)
    suggestions.value = data
  } catch (e) { console.error(e) }
}
function selectSuggestion(item){
  if (!codeInput.value.includes(item.code))
    codeInput.value = codeInput.value ? `${codeInput.value},${item.code}` : item.code
  searchInput.value = item.name
  showSuggestions.value = false
}
const handleBlur = () => setTimeout(() => showSuggestions.value = false, 200)

/* ───────── 지표 계산 & API 호출 ───────── */
function calcMetrics(history){
  const closes = history.map(p=>p.close)
  const ret = ((closes.at(-1)-closes[0])/closes[0])*100
  const logRets = closes.slice(1).map((c,i)=>Math.log(c/closes[i]))
  const mu = logRets.reduce((a,b)=>a+b,0)/logRets.length
  const var_ = logRets.reduce((a,b)=>a+(b-mu)**2,0)/(logRets.length-1)
  const vol = Math.sqrt(var_)*Math.sqrt(252)*100
  let peak = closes[0], mdd = 0
  closes.forEach(c=>{ peak=Math.max(peak,c); mdd=Math.min(mdd,(c-peak)/peak) })
  return { ret, vol:Math.abs(vol), mdd:Math.abs(mdd*100) }
}

async function fetchCompareData(){
  const codes = codeInput.value.split(',').map(c=>c.trim()).filter(Boolean)
  if (!codes.length) return alert('유효한 종목코드를 입력해주세요.')
  isLoading.value = true
  try{
    const { data } = await axios.post('/api/stock/compare/',{
      codes, start_date:startDate.value, end_date:endDate.value
    })
    results.value = data.map(i=>({ ...i, ...calcMetrics(i.history) }))
    await nextTick(); drawCharts()
  }catch(e){
    console.error(e); alert('비교 데이터를 불러오는 중 오류가 발생했습니다.')
  }finally{ isLoading.value=false }
}

/* ───────── 차트 전환/그리기 ───────── */
function switchChart(mode){ chartMode.value = mode; nextTick(drawCharts) }
function destroyAll(){ [lineChart,candleChart,volumeChart].forEach(c=>c&&c.destroy()) }
function drawCharts(){ destroyAll(); (chartMode.value==='line')?buildLineChart():buildCandleVolumeCharts() }

/* --- 라인 + 이동평균 --- */
function buildLineChart(){
  const datasets=[]
  results.value.forEach((item,idx)=>{
    const dates  = item.history.map(p=>p.date)
    const closes = item.history.map(p=>p.close)
    const makeMA = len=>closes.map((_,i,a)=>i<len-1?null:a.slice(i-len+1,i+1).reduce((s,v)=>s+v,0)/len)
    const color = `hsl(${idx*60},70%,50%)`
    datasets.push({
      label:item.name, data:dates.map((d,i)=>({x:d,y:closes[i]})),
      borderColor:color, borderWidth:2, pointRadius:1.5, fill:false,tension:.3,spanGaps:true
    })
    ;[5,20,60].forEach(len=>{
      if(closes.length<len) return
      const ma=makeMA(len)
      datasets.push({
        label:`${item.name} MA${len}`, data:dates.map((d,i)=>({x:d,y:ma[i]})),
        borderDash:[4,4], borderColor:color, borderWidth:1, fill:false, pointRadius:0, spanGaps:false
      })
    })
  })

  lineChart = new Chart(lineCanvas.value.getContext('2d'),{
    type:'line',
    data:{datasets},
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{position:'top'},tooltip:{mode:'index',intersect:false}},
      scales:{
        x:{type:'time',time:{unit:'day'},title:{display:true,text:'날짜'}},
        y:{title:{display:true,text:'종가 (원)'}}
      }
    }
  })
}

/* --- 캔들스틱 + 거래량 --- */
function buildCandleVolumeCharts(){
  const { history, name } = results.value[0]

  /* 🔥 barThickness 를 데이터 개수/캔버스 폭으로 산출 */
  const canvasWidth = candleCanvas.value.clientWidth || 600
  const barW = Math.max(3, Math.floor(canvasWidth / history.length * 0.6))

  const priceData = history.map(p=>({
    x:new Date(p.date), o:p.open, h:p.high, l:p.low, c:p.close
  }))

  candleChart = new Chart(candleCanvas.value.getContext('2d'),{
    type:'candlestick',
    data:{ datasets:[{
      label:name,
      data:priceData,
      parsing:false,
      upColor:'rgba(211,47,47,0.6)',   // 상승 빨간/투명도
      downColor:'rgba(38,166,154,0.6)',
      borderColor:'#424242',
      /** 🔥 폭 고정 */
      barThickness: barW,
      minBarLength: 1,
      borderWidth:1
    }]},
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{
        x:{type:'time',time:{unit:'day'},offset:true},
        y:{title:{display:true,text:'가격'}}
      }
    }
  })

  const volumeData = history.map(p=>({ x:new Date(p.date), y:p.volume }))
  volumeChart = new Chart(volumeCanvas.value.getContext('2d'),{
    type:'bar',
    data:{ datasets:[{
      label:'거래량', data:volumeData,
      backgroundColor:'rgba(33,150,243,0.45)',
      borderWidth:0, barPercentage:1, categoryPercentage:1
    }]},
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{
        x:{type:'time',time:{unit:'day'}},
        y:{title:{display:true,text:'거래량'},ticks:{callback:v=>v.toLocaleString()}}
      }
    }
  })
}
</script>

<style scoped>
.chart-box canvas{ display:block; }
</style>