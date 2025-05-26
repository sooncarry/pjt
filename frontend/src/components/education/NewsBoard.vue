<template>
  <div class="container my-5">
    <h2 class="h5 fw-bold mb-4">🚨 최신 금융 뉴스</h2>

    <div class="d-flex flex-column gap-4">
      <a
        v-for="item in newsList"
        :key="item.url"
        :href="item.url"
        target="_blank"
        rel="noopener"
        class="d-flex border rounded-4 shadow-sm overflow-hidden text-decoration-none"
      >
        <img
          :src="item.thumbnail || 'https://dummyimage.com/120x80/cccccc/ffffff&text=No+Image'"
          alt="썸네일"
          class="img-fluid object-fit-cover"
          style="width: 120px; height: 100px; object-fit: cover;"
        />
        <div class="p-3 flex-grow-1 text-dark">
          <h3 class="fw-semibold mb-1" style="font-size: 1rem;">
            {{ item.title }}
          </h3>
          <div class="text-muted small mb-1">
            {{ formatPublishedAt(item.published_at) }} · {{ item.press }}
          </div>
          <p class="text-muted small mb-0">
            {{ item.lede }}
          </p>
        </div>
      </a>
    </div>

    <div class="text-center mt-4">
      <button
        v-if="hasMore"
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
const loading  = ref(false)
const cursor   = ref(null)    // { before, last_id }
const hasMore  = ref(true)

const formatPublishedAt = isoString => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString('ko-KR', {
    timeZone: 'Asia/Seoul',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  })
}

async function fetchPage() {
  if (!hasMore.value || loading.value) return
  loading.value = true

  try {
    const params = { page_size: 20 }
    if (cursor.value) {
      params.before  = cursor.value.before
      params.last_id = cursor.value.last_id
    }

    const { data } = await axios.get('/api/education/breaking-news/', { params })

    if (!cursor.value) {
      newsList.value = data.results
    } else {
      newsList.value.push(...data.results)
    }

    hasMore.value = data.has_more
    cursor.value  = data.cursor

  } catch (err) {
    console.error('뉴스 로딩 실패:', err)
  } finally {
    loading.value = false
  }
}

function loadMore() {
  fetchPage()
}

onMounted(fetchPage)
</script>

<style scoped>
a {
  color: inherit; /* 텍스트도 어두운색 유지 */
}
</style>
