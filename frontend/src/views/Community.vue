<script setup>
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const posts = ref([])
const alertMsg = inject('alertMsg')
const alertType = inject('alertType')

// 현재 페이지 상태
const currentPage = ref(1)
const pageSize = 10

// 게시글 불러오기
const fetchPosts = async () => {
  try {
    const res = await axios.get('/api/boards/', {
      headers: {
        Authorization: undefined // 인증 헤더 제거 (읽기 요청이므로)
      }
    })

    // pagination 적용 여부에 따라 처리
    const data = Array.isArray(res.data) ? res.data : res.data.results
    posts.value = data || []
    currentPage.value = 1
  } catch (error) {
    console.error('❌ 게시글 불러오기 실패:', error)
    posts.value = []
  }
}

watch(() => route.params.category, fetchPosts)
onMounted(fetchPosts)

// 카테고리별 필터링
const filteredPosts = computed(() => {
  const cat = route.params.category
  return cat ? posts.value.filter(p => p.category === cat) : posts.value
})

// 페이징 계산
const totalPages = computed(() => Math.ceil(filteredPosts.value.length / pageSize))
const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredPosts.value.slice(start, start + pageSize)
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const categoryDisplayName = {
  stock: '주식방',
  deposit: '예적금방',
  saving: '저축방',
  free: '자유이야기방',
  worker: '직장인방',
}

// 글쓰기 버튼
const handleWriteClick = () => {
  const isLoggedIn = !!localStorage.getItem('access_token')
  if (!isLoggedIn) {
    alertMsg.value = '로그인이 필요합니다.'
    alertType.value = 'danger'
    setTimeout(() => {
      router.push('/login')
    }, 3000)
    return
  }

  const category = route.params.category || ''
  router.push(`/community/create?category=${category}`)
}
</script>

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
                  'text-dark': route.params.category,
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
                  'text-dark': route.params.category !== key,
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
            {{ route.params.category ? categoryDisplayName[route.params.category] : '전체글' }}
          </h4>
          <button
            @click="handleWriteClick"
            class="btn btn-primary btn-sm rounded-pill px-3"
          >
            글쓰기
          </button>
        </div>

        <!-- 게시글 존재 여부 -->
        <ul v-if="filteredPosts.length" class="list-group">
          <li
            v-for="post in paginatedPosts"
            :key="post.id"
            class="list-group-item list-group-item-action rounded-3 mb-2"
          >
            <router-link
              :to="`/community/${post.id}`"
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
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
              <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">이전</a>
            </li>
            <li
              class="page-item"
              v-for="page in totalPages"
              :key="page"
              :class="{ active: currentPage === page }"
            >
              <a class="page-link" href="#" @click.prevent="changePage(page)">
                {{ page }}
              </a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
              <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">다음</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  </div>
</template>

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
</style>
