<template>
  <div>
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab" @click="activeTab = tab" :class="{ active: activeTab === tab }">
        {{ tab }}
      </button>
    </div>
    <div class="tab-content mt-6">
      <KeywordConcepts v-if="activeTab === '금융 핵심 키워드 정리'" />
      <ProductKnowledge v-if="activeTab === '금융 상품에 대한 지식'" />
      <StockKnowledge v-if="activeTab === '주식에 대한 지식'" />
      <NewsBoard v-if="activeTab === '뉴스 모아보기'" />
      <QuizBoard v-if="activeTab === '퀴즈 (간단하게라도)'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import KeywordConcepts from '@/components/education/KeywordConcepts.vue'
import ProductKnowledge from '@/components/education/ProductKnowledge.vue'
import StockKnowledge from '@/components/education/StockKnowledge.vue'
import NewsBoard from '@/components/education/NewsBoard.vue'
import QuizBoard from '@/components/education/QuizBoard.vue'

const tabs = ['금융 핵심 키워드 정리', '금융 상품에 대한 지식', '주식에 대한 지식', '뉴스 모아보기', '퀴즈 (간단하게라도)']
const activeTab = ref(tabs[0])
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 12px;
  border-bottom: 2px solid #ccc;
}
.tabs button {
  padding: 10px 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.tabs button.active {
  border-bottom: 4px solid #2563eb; /* blue-600 */
  color: #2563eb;
}
</style>
