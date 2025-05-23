<template>
  <div class="p-4">
    <div class="mb-4">
      <input
        type="text"
        v-model="searchQuery"
        @input="handleInput"
        @keydown.enter="handleSearch"
        placeholder="금융 용어 검색"
        class="border px-4 py-2 rounded w-full"
      />
      <ul v-if="suggestions.length" class="bg-white border rounded mt-1 shadow">
        <li
          v-for="(suggestion, index) in suggestions"
          :key="index"
          @click="selectSuggestion(suggestion)"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
        >
          {{ suggestion }}
        </li>
      </ul>
    </div>

    <div v-if="recentSearches.length" class="mb-4">
      <h4 class="font-bold mb-1">최근 검색어</h4>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="(item, index) in recentSearches"
          :key="index"
          class="bg-gray-200 px-2 py-1 rounded cursor-pointer"
          @click="selectSuggestion(item)"
        >
          {{ item }}
        </span>
      </div>
    </div>

    <ul>
      <li
        v-for="(term, index) in paginatedTerms"
        :key="index"
        class="border-b py-2 cursor-pointer"
        @click="toggleDetail(index + (currentPage - 1) * perPage)"
      >
        <div class="font-semibold">{{ term.title }} ({{ term.eng_title }})</div>
        <div v-if="activeIndex === index + (currentPage - 1) * perPage" class="mt-1 text-sm text-gray-700">
          {{ term.content }}
        </div>
      </li>
    </ul>

    <div class="mt-4 flex justify-center gap-2">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="currentPage = page"
        class="px-3 py-1 border rounded"
        :class="{ 'bg-blue-500 text-white': currentPage === page }"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const terms = ref([])
const suggestions = ref([])
const activeIndex = ref(null)
const recentSearches = ref(JSON.parse(localStorage.getItem('recentSearches') || '[]'))
const currentPage = ref(1)
const perPage = 10

const fetchTerms = async () => {
  try {
    const response = await axios.get('/api/finance-terms/', {
      params: { q: searchQuery.value }
    })
    terms.value = response.data
    activeIndex.value = null
    updateSuggestions()
  } catch (error) {
    console.error('용어 불러오기 실패', error)
  }
}

const updateSuggestions = () => {
  const query = searchQuery.value.toLowerCase()
  suggestions.value = [...new Set(terms.value.map(t => t.title))]
    .filter(title => title.toLowerCase().includes(query))
    .slice(0, 10)
}

const handleInput = () => {
  updateSuggestions()
}

const handleSearch = () => {
  if (searchQuery.value && !recentSearches.value.includes(searchQuery.value)) {
    recentSearches.value.unshift(searchQuery.value)
    recentSearches.value = recentSearches.value.slice(0, 5)
    localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value))
  }
  fetchTerms()
  suggestions.value = []
}

const selectSuggestion = (text) => {
  searchQuery.value = text
  handleSearch()
}

const toggleDetail = (index) => {
  activeIndex.value = activeIndex.value === index ? null : index
}

const totalPages = computed(() => Math.ceil(terms.value.length / perPage))

const paginatedTerms = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return terms.value.slice(start, start + perPage)
})

watch(searchQuery, () => {
  updateSuggestions()
})

onMounted(() => {
  fetchTerms()
})
</script>
