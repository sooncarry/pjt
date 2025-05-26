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
            {{ formatPublishedAt(item.published_at) }} · {{ item.press }}
          </div>
          <div class="text-muted small">
            {{ item.lede }}
          </div>
        </div>
      </div>
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

// ISO → 한국시간 포맷터
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
    // 기본 page_size, 이후부터는 cursor 인자 포함
    const params = { page_size: 20 }
    if (cursor.value) {
      params.before  = cursor.value.before
      params.last_id = cursor.value.last_id
    }
    console.log('[fetchPage] params =', params)

    const { data } = await axios.get('/api/education/breaking-news/', { params })
    console.log('[fetchPage] response cursor =', data.cursor, 'has_more=', data.has_more)

    // 첫 로드면 새로, 이후면 이어 붙이기
    if (!cursor.value) {
      newsList.value = data.results
    } else {
      newsList.value.push(...data.results)
    }

    // 다음 로드 가능 여부 & 커서 업데이트
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

onMounted(() => {
  fetchPage()
})
</script>

<style scoped>
/* 필요하면 추가 스타일 */
</style>
