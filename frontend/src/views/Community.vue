<template>
  <section class="hero-section border-bottom">
    <div class="container">
      <p class="text-primary fw-semibold mb-3">금융 소통 공간</p>
      <h2 class="fw-bold mb-4">👨‍👩‍👧‍👦 커뮤니티</h2>
      <p class="h4 text-muted">
        관심 분야가 비슷한 사람들과 정보를 공유하고 즐겁게 소통하세요.
      </p>
    </div>
  </section>

  <div class="bg-light py-2 border-bottom text-muted text-sm">
    <div class="container">
      홈 &gt; 커뮤니티
    </div>
  </div>

  <div class="container my-5">
    <div class="row">
      <!-- 사이드바 -->
      <div class="col-md-3 mb-4">
        <div class="card shadow-sm border-0 rounded-4 p-3">
          <h5 class="fw-bold mb-3">커뮤니티 주제</h5>
          <ul class="list-unstyled">
            <li class="mb-2">
              <router-link
                to="/community"
                class="text-decoration-none"
                :class="{
                  'fw-bold text-primary': !route.params.category,
                  'text-dark': route.params.category
                }"
              >
                전체글
              </router-link>
            </li>
            <li
              v-for="(name, key) in categoryDisplayName"
              :key="key"
              class="mb-2"
            >
              <router-link
                :to="`/community/category/${key}`"
                class="text-decoration-none"
                :class="{
                  'fw-bold text-primary': route.params.category === key,
                  'text-dark': route.params.category !== key
                }"
              >
                {{ name }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- 게시글 목록 -->
      <div class="col-md-9">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="fw-semibold mb-0">
            {{ route.params.category
              ? categoryDisplayName[route.params.category]
              : '전체글' }}
          </h4>
          <button
            @click="handleWriteClick"
            class="btn btn-primary btn-sm rounded-pill px-3"
          >
            글쓰기
          </button>
        </div>

        <!-- 로딩 중 표시 -->
        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-border" role="status" />
          <div class="mt-2">로딩 중...</div>
        </div>

        <!-- 게시글이 로드된 후 -->
        <div v-else>
          <ul v-if="filteredPosts.length" class="list-group">
            <li
              v-for="post in paginatedPosts"
              :key="post.id"
              class="list-group-item list-group-item-action rounded-3 mb-2"
            >
              <!-- detail로 이동할 때 현재 페이지를 query로 전달 -->
              <router-link
                :to="{
                  name: 'PostDetail',
                  params: { id: post.id },
                  query: { page: currentPage }
                }"
                class="text-decoration-none text-dark"
              >
                {{ post.title }}
              </router-link>
            </li>
          </ul>
          <p v-else class="text-muted">해당 카테고리에 게시글이 없습니다.</p>

          <!-- 페이징 -->
          <nav class="mt-4" v-if="totalPages > 1">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: startPage === 1 }">
                <a class="page-link" href="#" @click.prevent="prevGroup">
                  이전
                </a>
              </li>
              <li
                class="page-item"
                v-for="page in visiblePages"
                :key="page"
                :class="{ active: currentPage === page }"
              >
                <a
                  class="page-link"
                  href="#"
                  @click.prevent="changePage(page)"
                >
                  {{ page }}
                </a>
              </li>
              <li
                class="page-item"
                :class="{ disabled: startPage + 4 >= totalPages }"
              >
                <a class="page-link" href="#" @click.prevent="nextGroup">
                  다음
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const posts = ref([])
const isLoading = ref(true)
const alertMsg = inject('alertMsg')
const alertType = inject('alertType')

// 페이지 사이즈와 현재 페이지 (query.page를 먼저 읽음)
const pageSize = 10
const currentPage = ref(parseInt(route.query.page) || 1)

// API 호출
const fetchPosts = async () => {
  isLoading.value = true
  try {
    const res = await axios.get('/api/boards/', {
      headers: { Authorization: undefined }
    })
    const data = Array.isArray(res.data) ? res.data : res.data.results
    posts.value = data || []
  } catch (err) {
    console.error('❌ 게시글 불러오기 실패:', err)
    posts.value = []
  } finally {
    isLoading.value = false
  }
}

// category가 바뀔 때 다시 로드
watch(() => route.params.category, () => {
  // query.page가 없으면 기본 1
  currentPage.value = parseInt(route.query.page) || 1
  fetchPosts()
})
onMounted(fetchPosts)

// query.page가 직접 바뀌면 currentPage 동기화
watch(
  () => route.query.page,
  (newPage) => {
    currentPage.value = parseInt(newPage) || 1
  }
)

// 필터링 & 페이징
const filteredPosts = computed(() => {
  const cat = route.params.category
  return cat
    ? posts.value.filter((p) => p.category === cat)
    : posts.value
})
const totalPages = computed(() =>
  Math.ceil(filteredPosts.value.length / pageSize)
)
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredPosts.value.slice(start, start + pageSize)
})

// 5개 단위 그룹 페이징
const startPage = computed(() =>
  Math.floor((currentPage.value - 1) / 5) * 5 + 1
)
const visiblePages = computed(() => {
  const start = startPage.value
  const end = Math.min(start + 4, totalPages.value)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

// 페이지 이동 함수: state + URL query 동시 업데이트
const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    router.replace({ query: { page } })
  }
}
const prevGroup = () => changePage(Math.max(startPage.value - 5, 1))
const nextGroup = () =>
  changePage(Math.min(startPage.value + 5, totalPages.value))

// 글쓰기 버튼
const categoryDisplayName = {
  stock: '주식방',
  deposit: '예적금방',
  saving: '저축방',
  free: '자유이야기방',
  worker: '직장인방'
}
const handleWriteClick = () => {
  const isLoggedIn = !!localStorage.getItem('access_token')
  if (!isLoggedIn) {
    alertMsg.value = '로그인이 필요합니다.'
    alertType.value = 'danger'
    setTimeout(() => router.push('/login'), 3000)
    return
  }
  router.push({
    path: '/community/create',
    query: { page: currentPage.value }
  })
}
</script>

<style scoped>
.hero-section {
  background-color: #D9D5FF;
  padding: 100px 0;
}
.hero-section .spinner-border {
  width: 3rem;
  height: 3rem;
}
@media (max-width: 768px) {
  .hero-section {
    padding: 60px 0;
  }
}
@media (max-width: 480px) {
  .hero-section {
    padding: 40px 0;
  }
}
</style>
