<template>
  <div class="p-6">
    <button
      @click="goBack"
      class="mb-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
    >
      ← 돌아가기
    </button>

    <div v-if="knowledge">
      <h2 class="text-2xl font-bold mb-4">{{ knowledge.title }}</h2>
      <img :src="knowledge.image" alt="상세 이미지" class="mb-4 w-full max-w-xl" />
      <p class="text-gray-700 whitespace-pre-line leading-relaxed">{{ knowledge.content }}</p>
    </div>
    <div v-else>
      <p>데이터를 불러오는 중입니다...</p>
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
        const data = response.data  // ✅ 여기가 누락됐던 부분
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
