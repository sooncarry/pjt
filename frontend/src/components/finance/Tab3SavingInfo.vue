<template>
  <div class="container my-4">
    <h2 class="fw-semibold mb-4">📂 정기적금 상품 목록</h2>

    <!-- 데이터가 있을 때 -->
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
            <tr v-for="(item, idx) in products" :key="idx">
              <td style="color: #444444; font-size: 1.2rem">{{ item.kor_co_nm }}</td>
              <td style="color: #5a45ff; font-size: 1.2rem">{{ item.fin_prdt_nm }}</td>
              <td style="color: #444444; font-size: 1.0rem">{{ item.join_way }}</td>
              <td style="color: #444444; font-size: 1.0rem">{{ item.mtrt_int }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 데이터 없을 때 -->
    <BaseAlert
      v-else-if="!isLoading && products.length === 0"
      type="info"
      title="상품 없음"
      message="불러온 적금 상품이 없습니다."
    />

    <!-- 로딩 중일 때 -->
    <BaseAlert
      v-else
      type="info"
      title="불러오는 중"
      message="정기적금 상품을 불러오는 중입니다..."
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
    const res = await axios.get('/api/finance/saving-products')
    products.value = res.data || []
  } catch (err) {
    console.error('❌ 적금 API 호출 실패:', err)
  } finally {
    isLoading.value = false
  }
})
</script>
