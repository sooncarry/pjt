<!-- src/components/CommentForm.vue -->
<template>
  <div class="comment-form">
    <textarea v-model="localContent" placeholder="댓글을 입력하세요"></textarea>
    <button @click="submit">{{ isEdit ? '수정' : '등록' }}</button>
    <button v-if="isEdit" @click="$emit('cancel')">취소</button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
const props = defineProps({
  content: String,
  isEdit: Boolean,
})
const emit = defineEmits(['submit', 'cancel'])

const localContent = ref(props.content || '')

watch(() => props.content, (newVal) => {
  localContent.value = newVal
})

const submit = () => {
  if (!localContent.value.trim()) return
  emit('submit', localContent.value)
  localContent.value = ''
}
</script>

<style scoped>
.comment-form textarea {
  width: 100%;
  height: 60px;
}
.comment-form button {
  margin-right: 0.5rem;
}
</style>
