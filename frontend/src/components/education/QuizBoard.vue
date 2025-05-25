<template>
  <div class="container my-5">
    <h2 class="h4 fw-bold mb-4">💡 금융 퀴즈</h2>

    <div v-if="loading" class="text-muted">문제를 불러오는 중입니다...</div>

    <div v-else-if="currentQuestion">
      <div class="card p-4 shadow-sm border-0 rounded-4">
        <p class="fw-semibold mb-3">
          {{ currentIndex + 1 }}. {{ currentQuestion.question }}
        </p>

        <div class="d-flex flex-column gap-2">
          <div v-for="(option, idx) in options" :key="idx" class="form-check">
            <label class="form-check-label d-flex align-items-center gap-2">
              <input
                type="radio"
                class="form-check-input"
                :value="idx"
                v-model="selectedAnswer"
                :disabled="answerSubmitted"
              />
              <span>{{ option?.toString().trim() || '보기 없음' }}</span>
            </label>
          </div>
        </div>

        <!-- 제출 후 결과 -->
        <div v-if="answerSubmitted" class="mt-4">
          <p :class="isCorrect ? 'text-success' : 'text-danger'" class="fw-semibold mb-2">
            {{ isCorrect ? '🎉 정답입니다!' : '❌ 틀렸습니다.' }}
          </p>
          <p class="text-muted small">💬 해설: {{ currentQuestion.explanation }}</p>

          <div class="d-flex gap-3 mt-4">
            <button class="btn btn-outline-secondary btn-sm rounded-pill" @click="stopQuiz">
              그만하기
            </button>
            <button class="btn btn-primary btn-sm rounded-pill" @click="nextQuestion">
              다음 문제
            </button>
          </div>
        </div>

        <!-- 제출 전 -->
        <div v-else class="mt-4">
          <button
            class="btn btn-success btn-sm rounded-pill"
            @click="submitAnswer"
            :disabled="selectedAnswer === null"
          >
            정답 제출
          </button>
        </div>
      </div>
    </div>

    <div v-else class="text-muted">모든 퀴즈를 완료했습니다 🎉</div>
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
const options = computed(() =>
  currentQuestion.value
    ? [currentQuestion.value.option1, currentQuestion.value.option2, currentQuestion.value.option3, currentQuestion.value.option4]
    : []
)

const isCorrect = computed(() => {
  return selectedAnswer.value === currentQuestion.value?.answer
})

const fetchQuizData = async () => {
  try {
    const res = await axios.get('/api/education/quiz/')
    quizList.value = res.data.sort(() => 0.5 - Math.random())
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
    quizList.value = [] // 퀴즈 종료
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
