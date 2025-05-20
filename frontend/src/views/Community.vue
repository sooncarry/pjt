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

// 라우트 변경될 때마다 목록 다시 필터링
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
  <div class="community">
    <aside class="sidebar">
      <h3>커뮤니티 주제</h3>
      <ul>
        <li><router-link to="/community">전체글</router-link></li>
        <li v-for="(name, key) in categoryDisplayName" :key="key">
          <router-link :to="`/community/category/${key}`">{{ name }}</router-link>
        </li>
      </ul>
    </aside>

    <main class="post-list">
      <h2>{{ route.params.category ? categoryDisplayName[route.params.category] : '전체글' }}</h2>
      <ul>
        <li v-for="post in filteredPosts" :key="post.id">
          <router-link :to="`/community/${post.id}`">{{ post.title }}</router-link>
        </li>
      </ul>
      <router-link :to="`/community/create?category=${route.params.category || ''}`">글쓰기</router-link>

    </main>
  </div>
</template>

<style scoped>
.community {
  display: flex;
  gap: 2rem;
}
.sidebar {
  width: 200px;
  background: #f5f5f5;
  padding: 1rem;
}
.post-list {
  flex-grow: 1;
}
</style>
