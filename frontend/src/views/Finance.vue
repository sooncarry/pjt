<template>
  <div class="finance-view">

    <!-- 상단 배너 -->
    <section class="bg-white py-10 border-bottom">
      <div class="container">
        <p class="text-primary fw-semibold mb-2" style="font-size: 0.9rem;">
          금융 상품 소개
        </p>
        <h2 class="h3 fw-bold mb-3">금융 상품</h2>
        <p class="text-muted">
          금융 상품에 대한 정보를 검색하고 맞춤형 상품을 추천받아보세요.
        </p>
      </div>
    </section>


    <!-- 경로 -->
    <div class="bg-light py-2 border-bottom text-muted text-sm">
      <div class="container">
        홈 &gt; 금융 상품
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
