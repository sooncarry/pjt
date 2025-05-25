<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const posts = ref([])

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
</script>

<template>
  <div class="container my-5">
    <div class="row">
      <!-- 사이드바 -->
      <div class="col-md-3 mb-4">
        <div class="card shadow-sm border-0 rounded-4 p-3">
          <h5 class="fw-bold mb-3">커뮤니티 주제</h5>
          <ul class="list-unstyled">
            <li class="mb-2">
              <router-link to="/community" class="text-decoration-none text-dark">
                전체글
              </router-link>
            </li>
            <li v-for="(name, key) in categoryDisplayName" :key="key" class="mb-2">
              <router-link
                :to="`/community/category/${key}`"
                class="text-decoration-none text-dark"
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
          <router-link
            :to="`/community/create?category=${route.params.category || ''}`"
            class="btn btn-primary btn-sm rounded-pill px-3"
          >
            글쓰기
          </router-link>
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
</style>
