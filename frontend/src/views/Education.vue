<template>
  <div class="education-view">
    <!-- 📌 상단 설명 영역 -->
    <section class="hero-section border-bottom">
      <div class="container">
        <p class="text-primary fw-semibold mb-3">금융 교육 콘텐츠</p>
        <h2 class="fw-bold mb-4">📘 금융 교육</h2>
        <p class="text-muted">
          금융 지식을 키우고 다양한 상품과 뉴스, 퀴즈를 통해 실력을 쌓아보세요.
        </p>
      </div>
    </section>

    <!-- 경로 -->
    <div class="bg-light py-2 border-bottom text-muted text-sm">
      <div class="container">
        홈 &gt; 금융 교육
      </div>
    </div>

    <!-- 탭 버튼 -->
    <div class="bg-white border-bottom shadow-sm">
      <div class="container d-flex flex-wrap gap-2 py-3 justify-content-center">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          @click="activeTab = tab.key"
          class="btn btn-sm rounded-pill fw-semibold px-4"
          :class="activeTab === tab.key ? 'btn-primary text-white' : 'btn-outline-primary'"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- 콘텐츠 영역 -->
    <div class="container my-4">
      <div class="card p-4 shadow-sm border-0 rounded-4">
        <component :is="activeTabComponent" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import FinanceGlossary from '@/components/education/FinanceGlossary.vue'
import ProductKnowledge from '@/components/education/ProductKnowledge.vue'
import StockKnowledge from '@/components/education/StockKnowledge.vue'
import NewsBoard from '@/components/education/NewsBoard.vue'
import QuizBoard from '@/components/education/QuizBoard.vue'

const tabs = [
  { key: 'glossary', label: '금융 핵심 키워드' },
  { key: 'products', label: '금융 상품에 대한 지식' },
  { key: 'stocks', label: '주식에 대한 지식' },
  { key: 'news', label: '최신 금융 뉴스' },
  { key: 'quiz', label: '금융 퀴즈' },
]

const activeTab = ref('glossary')

const activeTabComponent = computed(() => {
  return {
    glossary: FinanceGlossary,
    products: ProductKnowledge,
    stocks: StockKnowledge,
    news: NewsBoard,
    quiz: QuizBoard,
  }[activeTab.value]
})
</script>

<style scoped>
.hero-section {
  background-color: #edeaff;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 120px 0;
}

</style>