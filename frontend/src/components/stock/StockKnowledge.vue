<template>
  <div class="container my-4">
    <h3 class="h5 fw-bold mb-4">📘 주식 기초 지식 카드</h3>

    <div class="row g-4">
      <div
        v-for="(item, index) in knowledgeList"
        :key="item.id"
        class="col-12 col-sm-6 col-md-4"
      >
        <router-link
          :to="{ name: 'KnowledgeDetail', params: { id: item.id } }"
          class="text-decoration-none"
        >
          <div class="card h-100 shadow-sm border-0 rounded-4 overflow-hidden">
            <div class="position-relative" style="height: 180px;">
              <img
                :src="item.image"
                alt="stock concept"
                class="w-100 h-100 object-fit-cover border-bottom"
                @error="e => console.error('❌ 이미지 로딩 실패:', e.target.src)"
              />
              <div class="position-absolute top-0 start-0 bg-dark bg-opacity-50 text-white px-2 py-1 small rounded-end rounded-bottom m-2">
                {{ index + 1 | twoDigits }}
              </div>
            </div>
            <div class="card-body">
              <h5 class="card-title fw-semibold text-dark mb-2">{{ item.title }}</h5>
              <p class="card-text text-muted small">{{ item.description }}</p>
            </div>
          </div>
        </router-link>
      </div>
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
        const data = response.data

        this.knowledgeList = data.map(item => {
          if (item.image && item.image.startsWith('/media/')) {
            item.image = `http://localhost:8000${item.image}`
          }
          return item
        })
        console.log('✅ 이미지 목록 불러오기 완료:', this.knowledgeList.map(i => i.image))
      } catch (error) {
        console.error('❌ 주식 지식 데이터를 불러오는 데 실패했습니다:', error)
      }
    }
  }
}
</script>

<style scoped>
.object-fit-cover {
  object-fit: cover;
}
</style>
