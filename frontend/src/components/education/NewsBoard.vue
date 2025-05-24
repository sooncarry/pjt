<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">📢 최신 금융 뉴스</h2>

    <!-- 검색창 및 전체보기 버튼 -->
    <div class="mb-4 flex items-center space-x-2">
      <input
        v-model="search"
        @keyup.enter="fetchNews(1)"
        type="text"
        placeholder="검색어 입력 후 Enter"
        class="flex-1 border px-4 py-2 rounded"
      />
      <button
        v-if="search"
        @click="clearSearch"
        class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
      >
        전체보기
      </button>
    </div>

    <!-- 뉴스 목록 -->
    <div v-if="isLoading" class="text-gray-500">불러오는 중...</div>
    <div v-else-if="error" class="text-red-500">에러 발생: {{ error }}</div>
    <div v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
        <div
          v-for="item in newsList"
          :key="item.id"
          class="bg-white shadow rounded-lg overflow-hidden"
        >
          <img
            v-if="item.thumbnail"
            :src="item.thumbnail"
            alt=""
            class="w-full h-48 object-cover"
          />
          <div class="p-4">
            <h3 class="text-lg font-semibold line-clamp-2 mb-2" v-html="item.title"></h3>
            <p class="text-sm text-gray-700 line-clamp-3" v-html="item.summary"></p>
            <div class="text-xs text-gray-500 mt-2">
              {{ item.source }} · {{ formatDate(item.published_at) }}
            </div>
            <a
              :href="item.url"
              target="_blank"
              rel="noopener"
              class="mt-2 block text-blue-500 text-sm font-medium"
            >
              기사 보기 →
            </a>
          </div>
        </div>
      </div>

      <!-- 페이지네이션 -->
      <div class="flex justify-center items-center space-x-2 mb-6">
        <button
          v-if="startPage > 1"
          @click="fetchNews(startPage - 1)"
          class="px-2 py-1 border rounded hover:bg-gray-100"
        >
          ‹
        </button>

        <button
          v-for="page in pages"
          :key="page"
          @click="fetchNews(page)"
          class="px-3 py-1 border rounded hover:bg-gray-100"
          :class="{ 'bg-blue-500 text-white': page === currentPage }"
        >
          {{ page }}
        </button>

        <button
          v-if="endPage < totalPages"
          @click="fetchNews(endPage + 1)"
          class="px-2 py-1 border rounded hover:bg-gray-100"
        >
          ›
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

// Reactive state
const newsList = ref([])
const isLoading = ref(true)
const error = ref(null)
const search = ref('')
const currentPage = ref(1)
const totalPages = ref(1)

// Pagination group size
const pageGroupSize = 5

// Compute start and end page for pagination window
const startPage = computed(() => {
  return Math.floor((currentPage.value - 1) / pageGroupSize) * pageGroupSize + 1
})
const endPage = computed(() => {
  return Math.min(startPage.value + pageGroupSize - 1, totalPages.value)
})

// Array of page numbers to display
const pages = computed(() => {
  const arr = []
  for (let i = startPage.value; i <= endPage.value; i++) {
    arr.push(i)
  }
  return arr
})

// Fetch news from backend
const fetchNews = async (page = 1) => {
  isLoading.value = true
  error.value = null
  try {
    const res = await axios.get('/api/news/', {
      params: {
        page,
        search: search.value,
        display: 100  // 한 번에 최대 100개 가져오기
      },
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

// Clear search and reload all news
const clearSearch = () => {
  search.value = ''
  fetchNews(1)
}

// Format ISO date to 'YYYY.MM.DD HH:mm'
const formatDate = (iso) => {
  if (!iso) return ''
  const date = new Date(iso)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// Initial load
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
