<!-- BreakingNews.vue -->
<template>
  <div class="container my-5">
    <h2 class="h5 fw-bold mb-4">🚨 최신 금융 뉴스</h2>

    <!-- 📰 뉴스 카드들 -->
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

    <!-- 📎 더보기 -->
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

  <!-- ⬆️ 맨 위로 버튼 (고정) -->
  <button
    v-if="showTopBtn"
    class="scroll-top-btn btn btn-primary rounded-circle"
    @click="scrollToTop"
    aria-label="맨 위로"
  >
    ↑
  </button>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const newsList = ref([])
const loading  = ref(false)
const cursor   = ref(null)    // { before, last_id }
const hasMore  = ref(true)

/* 🕮 날짜 포맷 ---------------------------------------------------- */
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

/* 📑 페이지네이션 -------------------------------------------------- */
async function fetchPage() {
  if (!hasMore.value || loading.value) return
  loading.value = true

  try {
    const params = { page_size: 20 }
    if (cursor.value) Object.assign(params, cursor.value)

    const { data } = await axios.get('/api/education/breaking-news/', { params })

    cursor.value  = data.cursor
    hasMore.value = data.has_more
    newsList.value.push(...data.results)
  } catch (err) {
    console.error('뉴스 로딩 실패:', err)
  } finally {
    loading.value = false
  }
}
const loadMore = () => fetchPage()

/* ⬆️ 맨 위로 버튼 -------------------------------------------------- */
const showTopBtn = ref(false)

const checkScroll = () => {
  showTopBtn.value = window.scrollY > 400   // 400px 이상이면 표시
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/* 라이프사이클 ---------------------------------------------------- */
onMounted(() => {
  fetchPage()
  window.addEventListener('scroll', checkScroll)
  checkScroll()          // 초기 진입 시 판단
})

onUnmounted(() => {
  window.removeEventListener('scroll', checkScroll)
})
</script>

<style scoped>
/* 카드 링크 색상 유지 */
a { color: inherit; }

/* ⬆️ 맨 위로 버튼 스타일 */
.scroll-top-btn {
  position: fixed;
  bottom: 32px;
  right: 32px;
  width: 44px;
  height: 44px;
  font-size: 1.25rem;
  line-height: 1;
  z-index: 1080;          /* 카드·모달 위에 표시 */
  box-shadow: 0 2px 6px rgba(0, 0, 0, .25);
}
</style>
