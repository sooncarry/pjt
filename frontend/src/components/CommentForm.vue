<template>
  <div class="comment-form">
    <textarea v-model="localContent" placeholder="댓글을 입력하세요"></textarea>
    <button @click="submit">등록</button>
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
.comment-form textarea {
  width: 100%;
  height: 60px;
}
.comment-form button {
  margin-top: 0.5rem;
}
</style>