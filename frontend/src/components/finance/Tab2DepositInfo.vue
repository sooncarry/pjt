<template>
  <div class="container mt-4">
    <!-- 1) 필터 카드 -->
    <div class="card mb-4 p-3">
      <!-- 은행 체크박스 그리드 -->
      <div class="mb-4">
        <div class="row row-cols-2 row-cols-md-5 g-3">
          <div class="col">
            <div class="form-check">
              <input
                id="bank_all_deposit"
                class="form-check-input"
                type="checkbox"
                v-model="allBanksSelected"
                @change="toggleAllBanks"
              />
              <label class="form-check-label" for="bank_all_deposit">전체</label>
            </div>
          </div>
          <div class="col" v-for="bank in banks" :key="bank">
            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                :id="`bank_deposit_${bank}`"
                :value="bank"
                v-model="filter.banks"
              />
              <label class="form-check-label" :for="`bank_deposit_${bank}`">{{ bank }}</label>
            </div>
          </div>
        </div>
      </div>
      <hr />

      <!-- 이자 계산방식 라디오 -->
      <div class="mb-3">
        <label class="me-3">이자 계산방식</label>
        <div class="form-check form-check-inline" v-for="opt in calcOptions" :key="opt.value">
          <input
            class="form-check-input"
            type="radio"
            :id="`calc_deposit_${opt.value||'all'}`"
            :value="opt.value"
            v-model="filter.calcType"
          />
          <label class="form-check-label" :for="`calc_deposit_${opt.value||'all'}`">{{ opt.label }}</label>
        </div>
      </div>

      <!-- 만기 라디오 -->
      <div class="mb-3">
        <label class="me-3">만기</label>
        <div class="form-check form-check-inline" v-for="t in termOptions" :key="t.value">
          <input
            class="form-check-input"
            type="radio"
            :id="`term_deposit_${t.value||'all'}`"
            :value="t.value"
            v-model="filter.term"
          />
          <label class="form-check-label" :for="`term_deposit_${t.value||'all'}`">{{ t.label }}</label>
        </div>
      </div>

      <!-- 가입방식 라디오 -->
      <div class="mb-4">
        <label class="me-3">가입방식</label>
        <div class="form-check form-check-inline" v-for="w in joinWays" :key="w.value">
          <input
            class="form-check-input"
            type="radio"
            :id="`way_deposit_${w.value||'all'}`"
            :value="w.value"
            v-model="filter.joinWay"
          />
          <label class="form-check-label" :for="`way_deposit_${w.value||'all'}`">{{ w.label }}</label>
        </div>
      </div>

      <!-- 정렬 & 버튼 -->
      <div class="d-flex align-items-center">
        <span class="me-2 fw-semibold">정렬방식</span>
        <select
          v-model="filter.sortBy"
          class="form-select form-select-sm rounded-pill border me-2 w-auto"
        >
          <option value="kor_co_nm">은행명</option>
          <option value="basicRate">기본금리</option>
          <option value="maxRate">최고금리</option>
        </select>
        <select
          v-model="filter.sortOrder"
          class="form-select form-select-sm rounded-pill border me-3 w-auto"
        >
          <option value="asc">오름차순</option>
          <option value="desc">내림차순</option>
        </select>
        <button class="btn btn-primary btn-sm rounded-pill me-2" @click="onSearch">
          검색
        </button>
        <button class="btn btn-outline-secondary btn-sm rounded-pill" @click="onShowAll">
          전체보기
        </button>
      </div>
    </div>

    <!-- 2) 결과 영역 -->
    <div v-if="showResults">
      <h2 class="fw-semibold mb-4">📄 정기예금 상품 목록</h2>

      <!-- 로딩 -->
      <BaseAlert
        v-if="isLoading"
        type="info"
        title="로딩 중"
        message="정기예금 상품을 불러오는 중입니다..."
      />

      <!-- 데이터 테이블 -->
      <div v-else-if="products.length" class="table-responsive">
        <table class="table table-bordered align-middle">
          <thead class="table-light text-center">
            <tr>
              <th>은행명</th>
              <th>상품명</th>
              <th>가입방법</th>
              <th>만기 후 금리</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="item in products" :key="item.fin_prdt_cd">
              <tr>
                <td class="text-center">{{ item.kor_co_nm }}</td>
                <td
                  class="text-center text-primary"
                  style="cursor: pointer"
                  @click="toggleRow(item.fin_prdt_cd)"
                >
                  {{ item.fin_prdt_nm }}
                </td>
                <td class="text-center">{{ item.join_way }}</td>
                <td class="text-center">{{ item.intr_rate }}%</td>
              </tr>
              <!-- 🎯 토글 상세정보 (수정된 부분) -->
              <tr v-if="expanded[item.fin_prdt_cd]">
                <td colspan="4" class="bg-light text-start">
                  <ul class="mb-0 py-2 px-3">
                    <li><strong>상품 코드:</strong> {{ item.fin_prdt_cd }}</li>
                    <li><strong>공시월:</strong> {{ item.dcls_month }}</li>
                    <li><strong>계약 기간:</strong> {{ item.save_trm }}개월</li>
                    <li><strong>이자 종류:</strong> {{ item.intr_rate_type_nm }}</li>
                    <li><strong>기본 금리:</strong> {{ item.intr_rate }}%</li>
                    <li><strong>우대 금리:</strong> {{ item.intr_rate2 }}%</li>
                    <li v-if="item.spcl_cnd"><strong>우대 조건:</strong> {{ item.spcl_cnd }}</li>
                    <li v-if="item.join_member"><strong>가입 대상:</strong> {{ item.join_member }}</li>
                    <li v-if="item.max_limit !== null">
                      <strong>최대 한도:</strong> {{ item.max_limit.toLocaleString() }}원
                    </li>
                    <li v-if="item.etc_note"><strong>기타 안내:</strong> {{ item.etc_note }}</li>
                  </ul>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- 상품 없음 -->
      <BaseAlert
        v-else
        type="info"
        title="상품 없음"
        message="조건에 맞는 상품이 없습니다."
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import qs from 'qs'
import BaseAlert from '@/components/BaseAlert.vue'

const products = ref([])
const isLoading = ref(false)
const showResults = ref(false)
const expanded = reactive({})

// 필터 상태
const filter = reactive({
  banks: [],
  calcType: '',
  term: '',
  joinWay: '',
  sortBy: 'kor_co_nm',
  sortOrder: 'asc'
})
const allBanksSelected = ref(false)

// 옵션 데이터
const banks = [
  '한국산업은행','NH농협은행','신한은행','우리은행','SC제일은행','하나은행',
  'IBK기업은행','KB국민은행','한국씨티은행','Sh수협은행','iM뱅크(구 대구은행)',
  'BNK부산은행','광주은행','제주은행','전북은행','BNK경남은행','케이뱅크',
  '카카오뱅크','토스뱅크'
]
const calcOptions = [
  { label: '전체', value: '' },
  { label: '단리', value: '단리' },
  { label: '복리', value: '복리' }
]
const termOptions = [
  { label: '전체', value: '' },
  { label: '1개월', value: '1' },
  { label: '3개월', value: '3' },
  { label: '6개월', value: '6' },
  { label: '12개월', value: '12' },
  { label: '24개월', value: '24' },
  { label: '36개월', value: '36' }
]
const joinWays = [
  { label: '전체', value: '' },
  { label: '영업점', value: '영업점' },
  { label: '인터넷', value: '인터넷' },
  { label: '스마트폰', value: '스마트' },
  { label: '전화', value: '전화' },
  { label: '기타', value: '기타' }
]

// 전체 토글
watch(allBanksSelected, v => filter.banks = v ? [...banks] : [])
watch(() => filter.banks.length, l => allBanksSelected.value = l === banks.length)
function toggleAllBanks() {
  filter.banks = allBanksSelected.value ? [...banks] : []
}

// 행 토글
function toggleRow(code) {
  expanded[code] = !expanded[code]
}

// API 호출 및 병합/필터/정렬 (기존 로직 그대로)
async function fetchProducts(params = {}) {
  isLoading.value = true
  try {
    const res = await axios.get('/api/finance/deposit-products/', {
      params,
      paramsSerializer: p => qs.stringify(p, { arrayFormat: 'repeat' })
    })
    let list = res.data.baseList || []

    // 최고 금리만 남기기
    const map = {}
    list.forEach(item => {
      const r2 = parseFloat(item.intr_rate2 ?? item.intr_rate ?? 0)
      if (!map[item.fin_prdt_cd] || r2 > parseFloat(map[item.fin_prdt_cd].intr_rate2 ?? map[item.fin_prdt_cd].intr_rate ?? 0)) {
        map[item.fin_prdt_cd] = item
      }
    })
    list = Object.values(map)

    // 정렬
    const keyMap = { kor_co_nm:'kor_co_nm', basicRate:'intr_rate', maxRate:'intr_rate2' }
    const rev = filter.sortOrder === 'desc'
    list.sort((a,b) => {
      const A = keyMap[filter.sortBy]==='kor_co_nm' ? a.kor_co_nm : parseFloat(a[keyMap[filter.sortBy]] ?? 0)
      const B = keyMap[filter.sortBy]==='kor_co_nm' ? b.kor_co_nm : parseFloat(b[keyMap[filter.sortBy]] ?? 0)
      return (A<B?-1:A>B?1:0)*(rev?-1:1)
    })

    return list
  } finally {
    isLoading.value = false
  }
}

async function onSearch() {
  showResults.value = true
  Object.keys(expanded).forEach(k => delete expanded[k])
  products.value = await fetchProducts(filter)
}
async function onShowAll() {
  Object.assign(filter, {
    banks: [], calcType:'', term:'', joinWay:'',
    sortBy:'kor_co_nm', sortOrder:'asc'
  })
  allBanksSelected.value = false
  showResults.value = true
  Object.keys(expanded).forEach(k => delete expanded[k])
  products.value = await fetchProducts({})
}

// 초기 로드 (화면엔 숨김)
fetchProducts({}).then(() => {})
</script>

<style scoped>
.bg-light ul { list-style: none; padding-left: 0; }
.bg-light li + li { margin-top: .5rem; }
</style>
