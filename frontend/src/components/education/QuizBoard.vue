<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-6">💡 금융 퀴즈</h2>

    <div v-if="loading" class="text-gray-500">문제를 불러오는 중입니다...</div>

    <div v-else-if="currentQuestion">
      <div class="mb-4 border rounded p-4 shadow">
        <p class="font-semibold mb-2">
          {{ currentIndex + 1 }}. {{ currentQuestion.question }}
        </p>
        <div class="space-y-2">
          <div v-for="(option, idx) in options" :key="idx">
            <label class="flex items-center space-x-2">
              <input
                type="radio"
                :value="idx"
                v-model="selectedAnswer"
                :disabled="answerSubmitted"
              />
              <span>{{ option?.toString().trim() || '보기 없음' }}</span>
          </label>
        </div>
        </div>

        <div v-if="answerSubmitted" class="mt-4">
          <p :class="isCorrect ? 'text-green-600' : 'text-red-600'" class="font-semibold">
            {{ isCorrect ? '정답입니다!' : '틀렸습니다.' }}
          </p>
          <p class="text-sm mt-2 text-gray-700">해설: {{ currentQuestion.explanation }}</p>

          <div class="mt-4 flex gap-4">
            <button @click="stopQuiz" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">
              그만하기
            </button>
            <button @click="nextQuestion" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
              다음 문제
            </button>
          </div>
        </div>

        <div v-else class="mt-4">
          <button
            @click="submitAnswer"
            class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
            :disabled="selectedAnswer === null"
          >
            정답 제출
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-gray-500">퀴즈가 더 이상 없습니다.</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const quizList = ref([])
const currentIndex = ref(0)
const selectedAnswer = ref(null)
const answerSubmitted = ref(false)
const loading = ref(true)

const currentQuestion = computed(() => quizList.value[currentIndex.value])
const options = computed(() => currentQuestion.value
  ? [currentQuestion.value.option1, currentQuestion.value.option2, currentQuestion.value.option3, currentQuestion.value.option4]
  : [])

const isCorrect = computed(() => {
  return selectedAnswer.value === currentQuestion.value?.answer
})

const fetchQuizData = async () => {
  try {
    const res = await axios.get('/api/education/quiz/')
    quizList.value = res.data.sort(() => 0.5 - Math.random()) // 무작위 섞기
  } catch (err) {
    console.error('퀴즈 로딩 오류:', err)
  } finally {
    loading.value = false
  }
}

const submitAnswer = () => {
  answerSubmitted.value = true
}

const nextQuestion = () => {
  if (currentIndex.value < quizList.value.length - 1) {
    currentIndex.value += 1
    selectedAnswer.value = null
    answerSubmitted.value = false
  } else {
    quizList.value = [] // 모든 문제 끝나면 비움
  }
}

const stopQuiz = () => {
  quizList.value = []
}

onMounted(fetchQuizData)
</script>

<style scoped>
input[type='radio']:disabled + span {
  color: #999;
}
</style>
