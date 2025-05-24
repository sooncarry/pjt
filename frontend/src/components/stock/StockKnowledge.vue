<template>
  <div>
    <h3 class="text-2xl font-bold mb-6">📘 주식 기초 지식 카드</h3>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <router-link
        v-for="(item, index) in knowledgeList"
        :key="item.id"
        :to="{ name: 'KnowledgeDetail', params: { id: item.id } }"
        class="block"
      >
        <div class="rounded-lg overflow-hidden shadow hover:shadow-lg transition">
          <div class="relative h-48 bg-gray-200">
            <img
              :src="item.image"
              alt="stock concept"
              class="w-full h-full object-cover"
            />
            <div class="absolute top-2 left-2 bg-black bg-opacity-60 text-white text-xs px-2 py-1 rounded">
              {{ index + 1 | twoDigits }}
            </div>
          </div>
          <div class="p-4">
            <h4 class="text-lg font-semibold mb-1">{{ item.title }}</h4>
            <p class="text-sm text-gray-600">{{ item.description }}</p>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StockKnowledge',
  data() {
    return {
      knowledgeList: []
    }
  },
  filters: {
    twoDigits(val) {
      return val < 9 ? `0${val}` : val
    }
  },
  mounted() {
    this.fetchKnowledgeList()
  },
  methods: {
    async fetchKnowledgeList() {
      try {
        const response = await axios.get('/api/stock/knowledge/')
        this.knowledgeList = response.data
      } catch (error) {
        console.error('❌ 주식 지식 데이터를 불러오는 데 실패했습니다:', error)
      }
    }
  }
}
</script>

<style scoped>
</style>
