<template>
  <div>
    <h2 class="text-xl font-bold mb-4">정기예금 상품 목록</h2>

    <!-- 데이터 있는 경우 -->
    <table class="w-full border text-sm" v-if="!isLoading && products.length">
      <thead>
        <tr class="bg-gray-200">
          <th class="border px-2 py-1">은행명</th>
          <th class="border px-2 py-1">상품명</th>
          <th class="border px-2 py-1">가입방법</th>
          <th class="border px-2 py-1">만기 후 이자율</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in products" :key="item.fin_prdt_cd">
          <td class="border px-2 py-1">{{ item.kor_co_nm }}</td>
          <td class="border px-2 py-1">{{ item.fin_prdt_nm }}</td>
          <td class="border px-2 py-1">{{ item.join_way }}</td>
          <td class="border px-2 py-1">{{ item.mtrt_int }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 데이터 없는 경우 -->
    <div v-else-if="!isLoading && products.length === 0" class="text-gray-500">
      불러온 상품이 없습니다.
    </div>

    <!-- 로딩 중 -->
    <div v-else class="text-gray-400">
      불러오는 중입니다...
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      products: [],
      isLoading: true,
    }
  },
  async mounted() {
    try {
      const res = await axios.get('/api/deposit-products')
      console.log('✅ API 응답 결과:', res.data)
      this.products = res.data?.baseList || []
    } catch (err) {
      console.error('❌ API 호출 실패:', err)
    } finally {
      this.isLoading = false
    }
  }
}
</script>

<style scoped>
/* 필요 시 커스텀 스타일 추가 */
</style>