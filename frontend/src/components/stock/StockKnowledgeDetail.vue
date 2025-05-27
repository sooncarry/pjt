<template>
  <div class="container my-4"style="padding-top: 120px;" >
    <button
      @click="goBack"
      class="btn btn-outline-primary btn-sm rounded-pill mb-4 px-4"
    >
      ← 돌아가기
    </button>

    <div v-if="knowledge">
      <h2 class="h4 fw-bold mb-3">{{ knowledge.title }}</h2>
      <img
        :src="knowledge.image"
        alt="상세 이미지"
        class="img-fluid rounded mb-4 border"
        style="max-width: 640px;"
      />
      <p class="text-muted" style="white-space: pre-line; line-height: 1.7;">
        {{ knowledge.content }}
      </p>
    </div>

    <div v-else class="text-muted">
      데이터를 불러오는 중입니다...
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

export default {
  name: 'StockKnowledgeDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const knowledge = ref(null)

    const fetchDetail = async () => {
      try {
        const response = await axios.get(`/api/stock/knowledge/${route.params.id}/`)
        const data = response.data
        if (data.image && data.image.startsWith('/media/')) {
          data.image = `http://localhost:8000${data.image}`
        }
        knowledge.value = data
        console.log('✅ 이미지 URL 보정 후:', knowledge.value.image)
      } catch (err) {
        console.error('❌ 상세 정보를 불러오는 데 실패했습니다:', err)
      }
    }

    const goBack = () => {
      router.back()
    }

    onMounted(fetchDetail)

    return { knowledge, goBack }
  }
}
</script>

<style scoped>
</style>
