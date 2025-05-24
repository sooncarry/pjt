<template>
  <div class="p-6">
    <div class="mb-6 flex flex-col sm:flex-row sm:items-center gap-4">
      <div class="relative w-full sm:w-1/2">
        <input
          v-model="searchQuery"
          @input="onInput"
          @focus="showSuggestions = true"
          @keydown.enter="handleEnterKey"
          type="text"
          placeholder="검색어 입력"
          class="w-full border px-4 py-2 rounded"
        />
        <ul v-if="showSuggestions && suggestions.length" class="absolute z-10 bg-white border rounded mt-1 shadow w-full max-h-48 overflow-auto">
          <li
            v-for="(suggestion, index) in suggestions"
            :key="index"
            @mousedown.prevent="selectSuggestion(suggestion)"
            class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
          >
            {{ suggestion.title }}
          </li>
        </ul>

        <div class="mt-2 text-sm text-gray-600" v-if="recentSearches.length">
          <div class="font-medium mb-1">최근 검색어</div>
          <div class="flex gap-2 flex-wrap">
            <span
              v-for="(item, idx) in recentSearches"
              :key="idx"
              class="px-2 py-1 bg-gray-100 rounded cursor-pointer hover:bg-gray-200"
              @click="searchQuery = item; fetchTerms(); showSuggestions = false"
            >
              {{ item }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div
        v-for="(term, index) in paginatedTerms"
        :key="index"
        class="border-b py-2 cursor-pointer hover:bg-gray-50"
        @click="toggleDetail(index)"
      >
        <div class="font-semibold text-blue-700">{{ term.title }} <span class="text-sm text-gray-500">({{ term.eng_title || 'N/A' }})</span></div>
        <div v-if="activeIndex === index" class="text-sm text-gray-700 mt-1 whitespace-pre-line">{{ term.content }}</div>
      </div>
    </div>

    <div class="flex justify-center mt-6 gap-1">
      <button v-if="currentPageGroup > 1" @click="prevPageGroup" class="px-3 py-1 rounded border">이전</button>
      <button
        v-for="page in visiblePageNumbers"
        :key="page"
        :class="['px-3 py-1 rounded border', currentPage === page ? 'bg-blue-500 text-white' : 'bg-white text-gray-700']"
        @click="changePage(page)"
      >
        {{ page }}
      </button>
      <button v-if="currentPageGroup < totalPageGroups" @click="nextPageGroup" class="px-3 py-1 rounded border">다음</button>
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

// 최근 검색어 관리
const recentSearches = ref(JSON.parse(localStorage.getItem('recentSearches') || '[]'))
const saveRecentSearch = (term) => {
  const updated = [term, ...recentSearches.value.filter(t => t !== term)].slice(0, 8)
  recentSearches.value = updated
  localStorage.setItem('recentSearches', JSON.stringify(updated))
}

const fetchTerms = async () => {
  try {
    const response = await axios.get('/api/finance-terms/', {
      params: { q: searchQuery.value }
    })
    terms.value = response.data
    activeIndex.value = null
    currentPage.value = 1

    if (searchQuery.value.trim()) {
      saveRecentSearch(searchQuery.value)
    }
  } catch (error) {
    console.error('용어 불러오기 실패', error)
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

onMounted(() => {
  fetchTerms()
})
</script>

<style scoped>
input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #2563eb66;
}
</style>