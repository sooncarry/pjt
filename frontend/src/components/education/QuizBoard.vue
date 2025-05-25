<template>
  <div class="p-6 max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold mb-6">📊 금융 상식 퀴즈</h2>

    <!-- 로딩 중 -->
    <div v-if="isLoading" class="text-center py-10 text-gray-500">퀴즈 불러오는 중...</div>

    <!-- 퀴즈 문제 표시 -->
    <QuizItem
      v-else-if="currentIndex < quizzes.length"
      :quiz="quizzes[currentIndex]"
      :index="currentIndex"
      @answered="handleAnswer"
    />

    <!-- 퀴즈 완료 시 -->
    <div v-else class="text-center border p-6 rounded shadow">
      <h3 class="text-xl font-semibold mb-4">퀴즈 완료!</h3>
      <p class="text-lg mb-2">총 {{ quizzes.length }}문제 중 {{ score }}문제 정답</p>
      <button
        class="mt-4 px-4 py-2 bg-green-500 text-white rounded"
        @click="restartQuiz"
      >
        다시 풀기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import QuizItem from './QuizItem.vue'

const quizzes = ref([])
const currentIndex = ref(0)
const score = ref(0)
const isLoading = ref(true)

const fetchQuizzes = async () => {
  try {
    const res = await axios.get('/api/quiz/quiz/')
    quizzes.value = res.data
  } catch (error) {
    console.error('퀴즈 로딩 실패:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchQuizzes()
})

const handleAnswer = (isCorrect) => {
  if (isCorrect) score.value++
  setTimeout(() => currentIndex.value++, 1000)
}

const restartQuiz = () => {
  currentIndex.value = 0
  score.value = 0
  isLoading.value = true
  fetchQuizzes()
}
</script>
