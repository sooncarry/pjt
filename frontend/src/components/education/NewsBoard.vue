<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">🚨 속보 금융 뉴스</h2>
    <ul>
      <li
        v-for="item in newsList"
        :key="item.url"
        class="flex items-start mb-4"
      >
        <img
          :src="item.thumbnail || 'https://dummyimage.com/120x80/cccccc/ffffff&text=No+Image'"
          alt="썸네일"
          class="w-24 h-16 object-cover rounded mr-4"
        />
        <div class="flex-1">
          <a
            :href="item.url"
            target="_blank"
            rel="noopener"
            class="block font-semibold hover:underline text-gray-800"
          >
            {{ item.title }}
          </a>
          <div class="text-xs text-gray-500 mt-1">
            {{ item.published_at }} · {{ item.press }}
          </div>
          <div class="text-sm text-gray-700 mt-1">
            {{ item.lede }}
          </div>
        </div>
      </li>
    </ul>

    <button
      v-if="currentPage < totalPages"
      @click="loadMore"
      :disabled="loading"
      class="block mx-auto px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
    >
      기사 더보기
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsList    = ref([])
const currentPage = ref(1)
const totalPages  = ref(1)
const loading     = ref(false)

async function fetchPage(page = 1) {
  if (page > totalPages.value) return
  loading.value = true
  try {
    const { data } = await axios.get('/api/breaking-news/', { params: { page } })
    if (page === 1) newsList.value = data.results ?? data
    else            newsList.value.push(...(data.results ?? data))
    currentPage.value = data.current_page ?? page
    totalPages.value  = data.total_pages ?? 1
  } catch (e) {
    console.error('속보 뉴스 로딩 실패', e)
  } finally {
    loading.value = false
  }
}

function loadMore() {
  fetchPage(currentPage.value + 1)
}

onMounted(() => fetchPage())
</script>
