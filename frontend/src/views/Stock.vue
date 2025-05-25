<template>
  <div class="stock-view">
    <!-- 📌 핀크 스타일 상단 설명 영역 -->
    <section class="bg-white py-5 border-bottom">
      <div class="container">
        <p class="text-primary fw-semibold mb-1" style="font-size: 0.9rem;">주식 기초 정보</p>
        <h2 class="h3 fw-bold mb-2">📈 주식 정보</h2>
        <p class="text-muted">
          주식 기초 지식을 배우고, 현물 상품 비교 및 관심 종목 정보를 조회해보세요.
        </p>
      </div>
    </section>

    <!-- 경로 표시 -->
    <div class="bg-light py-2 border-bottom text-muted text-sm">
      <div class="container">
        홈 &gt; 주식
      </div>
    </div>

    <!-- 탭 메뉴 -->
    <div class="bg-white border-bottom shadow-sm">
      <div class="container d-flex flex-wrap gap-3 py-3 justify-content-center">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          class="btn"
          :class="[
            'btn-sm fw-semibold rounded-pill px-4',
            activeTab === tab.key ? 'btn-primary text-white' : 'btn-outline-primary'
          ]"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- 탭 내용 -->
    <div class="container my-4">
      <div class="card p-4 shadow-sm border-0 rounded-4">
        <component :is="activeTabComponent" />
      </div>
    </div>
  </div>
</template>

<script>
import StockKnowledge from '@/components/stock/StockKnowledge.vue'
import StockProductCompare from '@/components/stock/StockProductCompare.vue'
import StockInterestInfo from '@/components/stock/StockInterestInfo.vue'

export default {
  data() {
    return {
      activeTab: 'tab1',
      tabs: [
        { key: 'tab1', label: '주식에 대한 지식' },
        { key: 'tab2', label: '현물 상품 비교' },
        { key: 'tab3', label: '관심 종목 정보 검색' },
      ],
    }
  },
  computed: {
    activeTabComponent() {
      return {
        tab1: StockKnowledge,
        tab2: StockProductCompare,
        tab3: StockInterestInfo,
      }[this.activeTab]
    },
  },
}
</script>
