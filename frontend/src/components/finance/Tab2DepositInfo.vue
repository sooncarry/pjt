<template>
  <div class="container mt-4">
    <h2 class="h5 fw-semibold mb-4">📄 정기예금 상품 목록</h2>

    <!-- 데이터 있을 경우 -->
    <div v-if="!isLoading && products.length">
      <div class="table-responsive">
        <table class="table table-bordered align-middle text-center">
          <thead class="table-light">
            <tr>
              <th>은행명</th>
              <th>상품명</th>
              <th>가입방법</th>
              <th>만기 후 이자율</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in products" :key="item.fin_prdt_cd">
              <td>{{ item.kor_co_nm }}</td>
              <td>{{ item.fin_prdt_nm }}</td>
              <td>{{ item.join_way }}</td>
              <td>{{ item.mtrt_int }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 데이터 없음 -->
    <BaseAlert
      v-else-if="!isLoading && products.length === 0"
      type="info"
      title="상품 없음"
      message="불러온 상품이 없습니다."
    />

    <!-- 로딩 중 -->
    <BaseAlert
      v-else
      type="info"
      title="로딩 중"
      message="정기예금 상품을 불러오는 중입니다..."
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BaseAlert from '@/components/BaseAlert.vue'

const products = ref([])
const isLoading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('/api/finance/deposit-products')
    console.log('✅ API 응답 결과:', res.data)
    products.value = res.data?.baseList || []
  } catch (err) {
    console.error('❌ API 호출 실패:', err)
  } finally {
    isLoading.value = false
  }
})
</script>
