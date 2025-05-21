<template>
  <div class="stock-view">
    <!-- 상단 배너 -->
    <section
      class="relative bg-cover bg-center h-56 flex items-center justify-center"
      style="background-image: url('/stock-banner.jpg')"
    >
      <div class="text-white text-4xl font-bold bg-black bg-opacity-50 px-8 py-4 rounded">
        주식 정보
      </div>
    </section>

    <!-- 경로 표시 -->
    <div class="px-8 py-2 text-sm text-gray-500 bg-gray-50">
      홈 > 주식
    </div>

    <!-- 탭 메뉴 -->
    <div class="bg-blue-600 text-white flex justify-center space-x-4 text-sm font-medium">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :class="['py-3 px-6', activeTab === tab.key ? 'border-b-4 border-white' : '']"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 탭 내용 -->
    <div class="p-6">
      <component :is="activeTabComponent" />
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
