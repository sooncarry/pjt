<template>
  <div class="border rounded p-4 shadow">
    <h3 class="font-semibold mb-3 text-base">
      {{ index + 1 }}. {{ quiz.question }}
    </h3>

    <ul class="space-y-2">
      <li
        v-for="(option, i) in quiz.options"
        :key="i"
        @click="selectOption(i)"
        :class="[
          'p-2 border rounded cursor-pointer',
          selectedIndex === i ? 'bg-blue-100' : '',
          showAnswer && i === quiz.answer ? 'border-green-500' : '',
          showAnswer && selectedIndex === i && selectedIndex !== quiz.answer
            ? 'border-red-500 bg-red-50'
            : '',
        ]"
      >
        {{ option }}
      </li>
    </ul>

    <div class="mt-3">
      <button
        class="bg-blue-500 text-white px-4 py-2 rounded"
        @click="submitAnswer"
        :disabled="selectedIndex === null || showAnswer"
      >
        정답 확인
      </button>

      <p v-if="showAnswer" class="mt-2 text-sm text-gray-700">
        해설: {{ quiz.explanation }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  quiz: Object, // { question, options, answer, explanation }
  index: Number,
})

const emit = defineEmits(['answered'])

const selectedIndex = ref(null)
const showAnswer = ref(false)

const selectOption = (i) => {
  if (!showAnswer.value) {
    selectedIndex.value = i
  }
}

const submitAnswer = () => {
  if (selectedIndex.value !== null) {
    showAnswer.value = true
    const isCorrect = selectedIndex.value === props.quiz.answer
    emit('answered', isCorrect)
  }
}
</script>
