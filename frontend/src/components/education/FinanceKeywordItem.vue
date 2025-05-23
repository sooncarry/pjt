<template>
  <div class="border-b py-2">
    <div @click="toggle" class="cursor-pointer font-medium">
      {{ term.title }} <span v-if="term.eng_title" class="text-gray-500">({{ term.eng_title }})</span>
    </div>
    <div v-if="isOpen" class="mt-2 text-sm text-gray-700 whitespace-pre-line">
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
