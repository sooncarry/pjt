<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">📢 금융 뉴스 모아보기</h2>

    <!-- 검색창 -->
    <div class="mb-4">
      <input
        v-model="search"
        @keyup.enter="fetchNews(1)"
        type="text"
        placeholder="검색어 입력 후 Enter"
        class="w-full sm:w-1/2 border px-4 py-2 rounded"
      />
    </div>

    <!-- 뉴스 목록 -->
    <div v-if="isLoading" class="text-gray-500">불러오는 중...</div>
    <div v-else-if="error" class="text-red-500">에러 발생: {{ error }}</div>
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <div v-for="item in newsList" :key="item.id" class="bg-white shadow rounded-lg overflow-hidden">
          <img :src="item.thumbnail" alt="" class="w-full h-48 object-cover" />
          <div class="p-4">
            <h3 class="text-lg font-semibold line-clamp-2 mb-2">{{ item.title }}</h3>
            <p class="text-sm text-gray-700 line-clamp-3">{{ item.summary }}</p>
            <div class="text-xs text-gray-500 mt-2">{{ item.source }} · {{ formatDate(item.published_at) }}</div>
            <a :href="item.url" target="_blank" class="mt-2 block text-blue-500 text-sm font-medium">기사 보기 →</a>
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div class="flex justify-center space-x-2">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="fetchNews(page)"
          class="px-3 py-1 border rounded"
          :class="{ 'bg-blue-500 text-white': page === currentPage }"
        >
          {{ page }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsList = ref([])
const isLoading = ref(true)
const error = ref(null)
const search = ref('')
const currentPage = ref(1)
const totalPages = ref(1)

const fetchNews = async (page = 1) => {
  isLoading.value = true
  error.value = null
  try {
    const res = await axios.get('/api/news_list/', {
      params: { page, search: search.value },
    })
    newsList.value = res.data.results
    currentPage.value = res.data.current_page
    totalPages.value = res.data.total_pages
  } catch (err) {
    error.value = err.message || '뉴스 로딩 실패'
  } finally {
    isLoading.value = false
  }
}

const formatDate = (str) => new Date(str).toLocaleDateString('ko-KR')

onMounted(() => fetchNews())
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
