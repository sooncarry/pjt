<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  message: String,
  type: {
    type: String,
    default: 'success'
  },
  duration: {
    type: Number,
    default: 2000
  }
})

const visible = ref(true)

watch(
  () => props.message,
  () => {
    visible.value = true
    setTimeout(() => (visible.value = false), props.duration)
  },
  { immediate: true }
)
</script>

<template>
  <div v-if="visible" class="alert-box alert" :class="'alert-' + type">
    {{ message }}
  </div>
</template>
