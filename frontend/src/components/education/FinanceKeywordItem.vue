<template>
  <div class="glossary-item border-bottom py-2">
    <div
      class="cursor-pointer d-flex justify-content-between align-items-center"
      @click="toggle"
    >
      <div class="fw-semibold text-primary">
        {{ term.title }}
        <span v-if="term.eng_title" class="text-muted small">({{ term.eng_title }})</span>
      </div>
      <span class="text-muted small">{{ isOpen ? '▲' : '▼' }}</span>
    </div>

    <div v-if="isOpen" class="mt-2 text-muted small" style="white-space: pre-line;">
      {{ term.content }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  term: Object,
  isOpen: Boolean
})
const emit = defineEmits(['toggle'])
const toggle = () => emit('toggle')
</script>

<style scoped>
.glossary-item:hover {
  background-color: #f8f9fa;
}
.cursor-pointer {
  cursor: pointer;
}
</style>
