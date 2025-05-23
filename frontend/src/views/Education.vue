<template>
  <div class="p-6 max-w-5xl mx-auto">
    <!-- 탭 버튼 -->
    <div class="flex flex-wrap gap-3 border-b pb-2">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        :class="[
          'px-4 py-2 font-semibold transition-colors duration-200 rounded-t-lg',
          activeTab === tab
            ? 'text-blue-600 border-b-4 border-blue-600 bg-white'
            : 'text-gray-500 hover:text-blue-500'
        ]"
      >
        {{ tab }}
      </button>
    </div>

    <!-- 탭 콘텐츠 -->
    <div class="mt-6 bg-white shadow rounded-xl p-6">
      <FinanceGlossary v-if="activeTab === '금융 핵심 키워드 정리'" />
      <ProductKnowledge v-if="activeTab === '금융 상품에 대한 지식'" />
      <StockKnowledge v-if="activeTab === '주식에 대한 지식'" />
      <NewsBoard v-if="activeTab === '뉴스 모아보기'" />
      <QuizBoard v-if="activeTab === '퀴즈 (간단하게라도)'" />
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
  '금융 핵심 키워드 정리',
  '금융 상품에 대한 지식',
  '주식에 대한 지식',
  '뉴스 모아보기',
  '퀴즈 (간단하게라도)'
]
const activeTab = ref(tabs[0])
</script>
