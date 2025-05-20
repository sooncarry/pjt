<template>
  <div class="finance-view">
    <!-- 상단 배너 -->
    <section
      class="relative bg-cover bg-center h-56 flex items-center justify-center"
      style="background-image: url('/banner.jpg')"
    >
      <div class="text-white text-4xl font-bold bg-black bg-opacity-50 px-8 py-4 rounded">
        금융 상품
      </div>
    </section>

    <!-- 경로 -->
    <div class="px-8 py-2 text-sm text-gray-500 bg-gray-50">
      홈 > 금융 상품
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
import Tab1ProductIntro from '@/components/finance/Tab1ProductIntro.vue'
import Tab2DepositInfo from '@/components/finance/Tab2DepositInfo.vue'
import Tab3SavingInfo from '@/components/finance/Tab3SavingInfo.vue'
import Tab4ProductRecommend from '@/components/finance/Tab4ProductRecommend.vue'
import Tab5NearbyBanks from '@/components/finance/Tab5NearbyBanks.vue'

export default {
  data() {
    return {
      activeTab: 'tab1',
      tabs: [
        { key: 'tab1', label: '금융 상품 알아보기' },
        { key: 'tab2', label: '예금정보조회' },
        { key: 'tab3', label: '적금정보조회' },
        { key: 'tab4', label: '맞춤형상품추천' },
        { key: 'tab5', label: '근처은행위치 조회' },
      ],
    }
  },
  computed: {
    activeTabComponent() {
      return {
        tab1: Tab1ProductIntro,
        tab2: Tab2DepositInfo,
        tab3: Tab3SavingInfo,
        tab4: Tab4ProductRecommend,
        tab5: Tab5NearbyBanks,
      }[this.activeTab]
    },
  },
}
</script>
