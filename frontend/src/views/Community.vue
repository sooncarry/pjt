<template>
  <!-- Hero & Breadcrumb -->
  <section class="hero-section border-bottom">
    <div class="container">
      <p class="text-primary fw-semibold mb-3">금융 소통 공간</p>
      <h2 class="fw-bold mb-4">👨‍👨‍👧‍👦 커뮤니티</h2>
      <p class="h4 text-muted">
        관심 분야가 비슷한 사람들과 정보를 공유하고 즐겁게 소통하세요.
      </p>
    </div>
  </section>
  <div class="bg-light py-2 border-bottom text-muted text-sm">
    <div class="container">홈 &gt; 커뮤니티</div>
  </div>

  <!-- Main Content -->
  <div class="container my-5">
    <div class="row">
      <!-- Sidebar -->
      <div class="col-md-3 mb-4">
        <div class="card shadow-sm border-0 rounded-4 p-3">
          <h5 class="fw-bold mb-3">커뮤니티 주제</h5>
          <ul class="list-unstyled">
            <li class="mb-2">
              <router-link
                to="/community"
                class="sidebar-link"
                :class="!route.params.category ? 'fw-bold text-primary' : 'text-dark'"
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
                class="sidebar-link"
                :class="route.params.category === key ? 'fw-bold text-primary' : 'text-dark'"
              >
                {{ name }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- Posts List -->
      <div class="col-md-9">
        <!-- Tabs + Write Button on one line -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <ul class="nav nav-pills">
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'all' }"
                href="#"
                @click.prevent="switchTab('all')"
              >전체글</a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'hot' }"
                href="#"
                @click.prevent="switchTab('hot')"
              >🔥 HOT 게시글</a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                :class="{ active: activeTab === 'popular' }"
                href="#"
                @click.prevent="switchTab('popular')"
              >⭐ 인기글</a>
            </li>
          </ul>
          <button
            @click="handleWriteClick"
            class="btn btn-primary btn-sm rounded-pill px-3"
          >
            글쓰기
          </button>
        </div>

        <!-- Loading Spinner -->
        <div v-if="isLoading" class="text-center py-5">
          <div class="spinner-border" role="status"></div>
          <div class="mt-2">로딩 중...</div>
        </div>

        <!-- Posts Table -->
        <div v-else>
          <table v-if="filteredPosts.length" class="table table-hover">
            <thead>
              <tr>
                <th>제목</th>
                <th>글쓴이</th>
                <th>등록일</th>
                <th>조회</th>
                <th>추천</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="post in paginatedPosts"
                :key="post.id"
                class="align-middle"
              >
                <td>
                  <router-link
                    :to="{ name: 'PostDetail', params: { id: post.id }, query: { page: currentPage } }"
                    class="text-decoration-none text-dark"
                  >
                    {{ post.title }}
                  </router-link>
                </td>
                <td>{{ post.author_username }}</td>
                <td>{{ post.created_at }}</td>
                <td>{{ post.view_count }}</td>
                <td>{{ post.likes_count }}</td>
              </tr>
            </tbody>
          </table>

          <p v-else class="text-muted">게시글이 없습니다.</p>

          <!-- Pagination -->
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
                <a class="page-link" href="#" @click.prevent="changePage(page)">
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

          <!-- Search -->
          <div class="d-flex justify-content-center align-items-center mt-3">
            <select v-model="searchBy" class="form-select w-auto me-2">
              <option value="both">제목+내용</option>
              <option value="title">제목</option>
              <option value="content">내용</option>
            </select>
            <input
              v-model="searchQuery"
              @keyup.enter="applySearch"
              type="text"
              class="form-control me-2"
              style="max-width: 250px;"
              placeholder="검색어 입력"
            />
            <button class="btn btn-primary text-nowrap" @click="applySearch">
              검색하기
            </button>
          </div>
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
const alertMsg = inject('alertMsg')
const alertType = inject('alertType')

// 상태
const posts = ref([])
const hotPosts = ref([])
const popularPosts = ref([])
const isLoading = ref(false)

// 페이징
const pageSize = 10
const currentPage = ref(parseInt(route.query.page) || 1)

// 검색
const searchQuery = ref('')
const searchBy = ref('both')
const appliedPosts = ref([])
const searchApplied = ref(false)

// 카테고리
const categoryDisplayName = {
  stock: '주식방',
  deposit: '예적금방',
  saving: '저축방',
  free: '자유이야기방',
  worker: '직장인방'
}

// 탭 상태
const activeTab = ref('all')

// API 호출
const fetchAll = async () => {
  isLoading.value = true
  try {
    const res = await axios.get('/api/boards/')
    posts.value = Array.isArray(res.data) ? res.data : res.data.results
  } finally {
    isLoading.value = false
    resetSearch()
  }
}

const fetchHot = async () => {
  isLoading.value = true
  try {
    // 백엔드 기본 limit=10 사용
    const res = await axios.get('/api/boards/', {
      params: { filter: 'hot', period: 'week' }
    })
    hotPosts.value = Array.isArray(res.data) ? res.data : res.data.results
  } finally {
    isLoading.value = false
    resetSearch()
  }
}

const fetchPopular = async () => {
  isLoading.value = true
  try {
    // 백엔드 기본 minCount=100 사용
    const res = await axios.get('/api/boards/', {
      params: { filter: 'popular' }
    })
    popularPosts.value = Array.isArray(res.data) ? res.data : res.data.results
  } finally {
    isLoading.value = false
    resetSearch()
  }
}

// 탭 전환
function switchTab(tab) {
  activeTab.value = tab
  currentPage.value = 1
  if (tab === 'all') fetchAll()
  else if (tab === 'hot') fetchHot()
  else if (tab === 'popular') fetchPopular()
}

// 초기 로드
onMounted(() => switchTab('all'))

// 검색 초기화
function resetSearch() {
  appliedPosts.value = []
  searchApplied.value = false
  searchQuery.value = ''
}

// 검색 적용
function applySearch() {
  const q = searchQuery.value.trim().toLowerCase()
  let list = sourcePosts.value

  if (q) {
    list = list.filter(p => {
      const t = p.title.toLowerCase()
      const c = p.content.toLowerCase()
      if (searchBy.value === 'title') return t.includes(q)
      if (searchBy.value === 'content') return c.includes(q)
      return t.includes(q) || c.includes(q)
    })
  }

  appliedPosts.value = list
  searchApplied.value = true
  currentPage.value = 1
}

// 원본 리스트 (탭 + 카테고리 적용)
const sourcePosts = computed(() => {
  let list = posts.value
  if (activeTab.value === 'hot') list = hotPosts.value
  else if (activeTab.value === 'popular') list = popularPosts.value

  if (route.params.category) {
    list = list.filter(p => p.category === route.params.category)
  }
  return list
})

// 최종 표시 리스트
const filteredPosts = computed(() =>
  searchApplied.value ? appliedPosts.value : sourcePosts.value
)

// 페이징 계산
const totalPages = computed(() => Math.ceil(filteredPosts.value.length / pageSize))
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredPosts.value.slice(start, start + pageSize)
})

// 그룹 페이징
const startPage = computed(() => Math.floor((currentPage.value - 1) / 5) * 5 + 1)
const visiblePages = computed(() => {
  const end = Math.min(startPage.value + 4, totalPages.value)
  return Array.from({ length: end - startPage.value + 1 }, (_, i) => startPage.value + i)
})
const changePage = page => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    router.replace({ query: { page } })
  }
}
const prevGroup = () => changePage(Math.max(startPage.value - 5, 1))
const nextGroup = () => changePage(Math.min(startPage.value + 5, totalPages.value))

// 글쓰기 이동
const handleWriteClick = () => {
  if (!localStorage.getItem('access_token')) {
    alertMsg.value = '로그인이 필요합니다.'
    alertType.value = 'danger'
    setTimeout(() => router.push('/login'), 3000)
    return
  }
  router.push({ path: '/community/create', query: { page: currentPage.value } })
}

// 탭 라벨
const activeTabLabel = computed(() => {
  if (activeTab.value === 'hot') return '🔥 HOT 게시글'
  if (activeTab.value === 'popular') return '⭐ 인기글'
  return route.params.category
    ? categoryDisplayName[route.params.category]
    : '전체글'
})
</script>

<style scoped>
.hero-section {
  background-color: #D9D5FF;
  padding: 100px 0;
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

/* 사이드바 링크 밑줄 제거 */
.sidebar-link {
  text-decoration: none !important;
}
</style>
