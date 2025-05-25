<template>
  <div class="container my-5">
    <!-- 검색 영역 -->
    <div class="mb-4">
      <div class="position-relative">
        <input
          v-model="searchQuery"
          @input="onInput"
          @focus="showSuggestions = true"
          @keydown.enter="handleEnterKey"
          type="text"
          class="form-control form-control-sm rounded-pill px-4"
          placeholder="🔍 금융 용어 검색"
        />
        <!-- 자동완성 목록 -->
        <ul
          v-if="showSuggestions && suggestions.length"
          class="list-group position-absolute w-100 mt-1 z-3"
        >
          <li
            v-for="(suggestion, index) in suggestions"
            :key="index"
            class="list-group-item list-group-item-action"
            @mousedown.prevent="selectSuggestion(suggestion)"
          >
            {{ suggestion.title }}
          </li>
        </ul>
      </div>

      <!-- 최근 검색어 -->
      <div v-if="recentSearches.length" class="mt-2 small text-muted">
        <div class="fw-semibold mb-1">최근 검색어</div>
        <div class="d-flex gap-2 flex-wrap">
          <span
            v-for="(item, idx) in recentSearches"
            :key="idx"
            class="badge text-bg-light px-2 py-1 rounded-pill cursor-pointer"
            @click="searchQuery = item; fetchTerms(); showSuggestions = false"
          >
            {{ item }}
          </span>
        </div>
      </div>
    </div>

    <!-- 용어 리스트 -->
    <div class="card p-4 shadow-sm border-0 rounded-4">
      <div
        v-for="(term, index) in paginatedTerms"
        :key="index"
        class="border-bottom py-2 cursor-pointer"
        @click="toggleDetail(index)"
      >
        <div class="fw-semibold text-primary">
          {{ term.title }}
          <span class="text-muted small">({{ term.eng_title || 'N/A' }})</span>
        </div>
        <div
          v-if="activeIndex === index"
          class="text-muted small mt-1"
          style="white-space: pre-line;"
        >
          {{ term.content }}
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="d-flex justify-content-center gap-1 mt-4">
      <button
        v-if="currentPageGroup > 1"
        class="btn btn-outline-secondary btn-sm rounded-pill"
        @click="prevPageGroup"
      >
        ◀ 이전
      </button>
      <button
        v-for="page in visiblePageNumbers"
        :key="page"
        @click="changePage(page)"
        :class="['btn btn-sm rounded-pill', currentPage === page ? 'btn-primary' : 'btn-outline-secondary']"
      >
        {{ page }}
      </button>
      <button
        v-if="currentPageGroup < totalPageGroups"
        class="btn btn-outline-secondary btn-sm rounded-pill"
        @click="nextPageGroup"
      >
        다음 ▶
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const terms = ref([])
const suggestions = ref([])
const showSuggestions = ref(false)
const activeIndex = ref(null)
const currentPage = ref(1)
const itemsPerPage = 20

const recentSearches = ref(JSON.parse(localStorage.getItem('recentSearches') || '[]'))
const saveRecentSearch = (term) => {
  const updated = [term, ...recentSearches.value.filter(t => t !== term)].slice(0, 8)
  recentSearches.value = updated
  localStorage.setItem('recentSearches', JSON.stringify(updated))
}

const fetchTerms = async () => {
  try {
    const res = await axios.get('/api/finance-terms/', {
      params: { q: searchQuery.value }
    })
    terms.value = res.data
    activeIndex.value = null
    currentPage.value = 1
    if (searchQuery.value.trim()) saveRecentSearch(searchQuery.value)
  } catch (err) {
    console.error('❌ 용어 불러오기 실패', err)
  }
}

const onInput = () => {
  if (!searchQuery.value.trim()) {
    suggestions.value = []
    return
  }
  suggestions.value = terms.value.filter(term =>
    term.title.includes(searchQuery.value) ||
    (term.eng_title && term.eng_title.toLowerCase().includes(searchQuery.value.toLowerCase()))
  ).slice(0, 10)
}

const selectSuggestion = (suggestion) => {
  searchQuery.value = suggestion.title
  showSuggestions.value = false
  fetchTerms()
}

const handleEnterKey = () => {
  showSuggestions.value = false
  fetchTerms()
}

const toggleDetail = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index
}

const paginatedTerms = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return terms.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(terms.value.length / itemsPerPage))
const pageGroupSize = 5
const currentPageGroup = computed(() => Math.ceil(currentPage.value / pageGroupSize))
const totalPageGroups = computed(() => Math.ceil(totalPages.value / pageGroupSize))

const visiblePageNumbers = computed(() => {
  const start = (currentPageGroup.value - 1) * pageGroupSize + 1
  return Array.from({ length: Math.min(pageGroupSize, totalPages.value - start + 1) }, (_, i) => start + i)
})

const changePage = (page) => {
  currentPage.value = page
  activeIndex.value = null
}
const prevPageGroup = () => {
  if (currentPageGroup.value > 1) {
    currentPage.value = (currentPageGroup.value - 2) * pageGroupSize + 1
    activeIndex.value = null
  }
}
const nextPageGroup = () => {
  if (currentPageGroup.value < totalPageGroups.value) {
    currentPage.value = currentPageGroup.value * pageGroupSize + 1
    activeIndex.value = null
  }
}

onMounted(fetchTerms)
</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
