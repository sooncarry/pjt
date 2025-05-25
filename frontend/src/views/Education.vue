<template>
  <div class="container my-5">
    <!-- 탭 메뉴 -->
    <div class="d-flex flex-wrap gap-2 border-bottom pb-2 mb-4">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        class="btn btn-sm rounded-pill fw-semibold"
        :class="activeTab === tab ? 'btn-primary' : 'btn-outline-secondary'"
      >
        {{ tab }}
      </button>
    </div>

    <!-- 콘텐츠 영역 -->
    <div class="card p-4 shadow-sm border-0 rounded-4">
      <FinanceGlossary v-if="activeTab === '금융 핵심 키워드'" />
      <ProductKnowledge v-if="activeTab === '금융 상품에 대한 지식'" />
      <StockKnowledge v-if="activeTab === '주식에 대한 지식'" />
      <NewsBoard v-if="activeTab === '최신 금융 뉴스'" />
      <QuizBoard v-if="activeTab === '금융 퀴즈'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FinanceGlossary from '@/components/education/FinanceGlossary.vue'
import ProductKnowledge from '@/components/education/ProductKnowledge.vue'
import StockKnowledge from '@/components/education/StockKnowledge.vue'
import NewsBoard from '@/components/education/NewsBoard.vue'
import QuizBoard from '@/components/education/QuizBoard.vue'

const tabs = [
  '금융 핵심 키워드',
  '금융 상품에 대한 지식',
  '주식에 대한 지식',
  '최신 금융 뉴스',
  '금융 퀴즈'
]

const activeTab = ref(tabs[0])
</script>
