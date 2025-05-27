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
              <div
                class="position-absolute top-0 start-0 bg-dark bg-opacity-50 text-white px-2 py-1 small rounded-end rounded-bottom m-2"
              >
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

    <!-- 페이지네이션이 있는 경우 추가 로드 버튼 -->
    <div class="text-center mt-4" v-if="nextUrl">
      <button class="btn btn-outline-primary" @click="loadMore">
        더보기
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StockKnowledge',
  data() {
    return {
      knowledgeList: [],
      nextUrl: null,
    }
  },
  filters: {
    twoDigits(val) {
      return val < 9 ? `0${val + 1}` : val + 1
    }
  },
  mounted() {
    this.fetchKnowledgeList()
  },
  methods: {
    async fetchKnowledgeList(url = '/api/stock/knowledge/?page_size=100') {
      try {
        const response = await axios.get(url)
        // DRF가 pagination 쓸 때는 results, 아닐 땐 바로 data
        const items = response.data.results || response.data
        // 이미지 URL 절대경로 처리
        const fixed = items.map(item => {
          if (item.image && item.image.startsWith('/media/')) {
            item.image = `http://localhost:8000${item.image}`
          }
          return item
        })
        // 기존 데이터에 합치기
        this.knowledgeList.push(...fixed)
        // 다음 페이지 URL 저장 (없으면 null)
        this.nextUrl = response.data.next
      } catch (error) {
        console.error('❌ 주식 지식 데이터를 불러오는 데 실패했습니다:', error)
      }
    },
    loadMore() {
      if (this.nextUrl) {
        this.fetchKnowledgeList(this.nextUrl)
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
