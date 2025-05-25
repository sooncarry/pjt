<template>
  <div class="card p-4 shadow-sm border-0 rounded-4 mb-4">
    <h3 class="fw-semibold mb-3 fs-6">
      {{ index + 1 }}. {{ quiz.question }}
    </h3>

    <ul class="list-unstyled">
      <li
        v-for="(option, i) in quiz.options"
        :key="i"
        @click="selectOption(i)"
        :class="[
          'px-3 py-2 mb-2 border rounded-pill',
          'cursor-pointer transition',
          selectedIndex === i && !showAnswer ? 'bg-primary text-white border-primary' : '',
          showAnswer && i === quiz.answer ? 'border-success text-success fw-semibold' : '',
          showAnswer && selectedIndex === i && selectedIndex !== quiz.answer
            ? 'border-danger bg-danger bg-opacity-10 text-danger'
            : ''
        ]"
        style="user-select: none;"
      >
        {{ option }}
      </li>
    </ul>

    <div class="mt-3">
      <button
        class="btn btn-sm rounded-pill"
        :class="showAnswer ? 'btn-outline-secondary' : 'btn-primary text-white'"
        @click="submitAnswer"
        :disabled="selectedIndex === null || showAnswer"
      >
        정답 확인
      </button>

      <p v-if="showAnswer" class="mt-3 small text-muted">
        💬 해설: {{ quiz.explanation }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  quiz: Object,
  index: Number,
})
const emit = defineEmits(['answered'])

const selectedIndex = ref(null)
const showAnswer = ref(false)

const selectOption = (i) => {
  if (!showAnswer.value) selectedIndex.value = i
}

const submitAnswer = () => {
  if (selectedIndex.value !== null) {
    showAnswer.value = true
    const isCorrect = selectedIndex.value === props.quiz.answer
    emit('answered', isCorrect)
  }
}
</script>
