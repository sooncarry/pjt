<script setup>
import { ref, watch, onMounted, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const posts = ref([])

const alertMsg = inject('alertMsg')
const alertType = inject('alertType')

const fetchPosts = async () => {
  const res = await axios.get('/api/boards/')
  posts.value = res.data
}

watch(() => route.params.category, fetchPosts)
onMounted(fetchPosts)

const filteredPosts = computed(() => {
  const cat = route.params.category
  return cat ? posts.value.filter(p => p.category === cat) : posts.value
})

const categoryDisplayName = {
  stock: '주식방',
  deposit: '예적금방',
  saving: '저축방',
  free: '자유이야기방',
  worker: '직장인방',
}

// 글쓰기 버튼 클릭 시 로그인 여부 확인
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
  <!-- 상단 배너 -->
  <section class="hero-section border-bottom">
    <div class="container">
      <p class="text-primary fw-semibold mb-3">금융 소통 공간</p>
      <h2 class="fw-bold mb-4">👨‍👩‍👧‍👦 커뮤니티</h2>
      <p class="h4 text-muted">
        관심 분야가 비슷한 사람들과 정보를 공유하고 즐겁게 소통하세요.
      </p>
    </div>
  </section>


  <!-- 경로 -->
  <div class="bg-light py-2 border-bottom text-muted text-sm">
    <div class="container">
      홈 &gt; 커뮤니티
    </div>
  </div>
  <div class="container my-5">
    
    <div class="row">
      <!-- 사이드바 -->
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

        <ul class="list-group">
          <li
            v-for="post in filteredPosts"
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero-section {
  background-color: #D9D5FF;
  padding: 100px 0; /* 기본 높이용 패딩 */
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

