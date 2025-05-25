<template>
  <div class="comment-form card p-3 border-0 shadow-sm rounded-4 mb-3">
    <textarea
      v-model="localContent"
      placeholder="댓글을 입력하세요"
      class="form-control form-control-sm mb-2"
      rows="3"
    ></textarea>
    <div class="text-end">
      <button
        class="btn btn-primary btn-sm rounded-pill px-3"
        @click="submit"
      >
        등록
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({ content: String })
const emit = defineEmits(['submit'])

const localContent = ref(props.content || '')

const submit = () => {
  if (!localContent.value.trim()) return
  emit('submit', localContent.value)
  localContent.value = ''
}
</script>

<style scoped>
</style>
