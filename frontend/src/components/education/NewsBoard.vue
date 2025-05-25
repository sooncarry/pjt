<template>
  <div class="container my-5">
    <h2 class="h5 fw-bold mb-4">🚨 속보 금융 뉴스</h2>

    <div class="d-flex flex-column gap-4">
      <div
        v-for="item in newsList"
        :key="item.url"
        class="d-flex border rounded-4 shadow-sm overflow-hidden"
      >
        <img
          :src="item.thumbnail || 'https://dummyimage.com/120x80/cccccc/ffffff&text=No+Image'"
          alt="썸네일"
          class="img-fluid object-fit-cover"
          style="width: 120px; height: 100px; object-fit: cover;"
        />
        <div class="p-3 flex-grow-1">
          <a
            :href="item.url"
            target="_blank"
            rel="noopener"
            class="fw-semibold text-dark text-decoration-none d-block mb-1"
          >
            {{ item.title }}
          </a>
          <div class="text-muted small mb-1">
            {{ item.published_at }} · {{ item.press }}
          </div>
          <div class="text-muted small">
            {{ item.lede }}
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <button
        v-if="currentPage < totalPages"
        @click="loadMore"
        :disabled="loading"
        class="btn btn-outline-primary btn-sm rounded-pill px-4"
      >
        {{ loading ? '로딩 중...' : '📎 더보기' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsList = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const loading = ref(false)

async function fetchPage(page = 1) {
  if (page > totalPages.value) return
  loading.value = true
  try {
    const { data } = await axios.get('/api/education/breaking-news/', { params: { page } })
    if (page === 1) newsList.value = data.results ?? data
    else newsList.value.push(...(data.results ?? data))
    currentPage.value = data.current_page ?? page
    totalPages.value = data.total_pages ?? 1
  } catch (e) {
    console.error('❌ 속보 뉴스 로딩 실패:', e)
  } finally {
    loading.value = false
  }
}

function loadMore() {
  fetchPage(currentPage.value + 1)
}

onMounted(() => fetchPage())
</script>
