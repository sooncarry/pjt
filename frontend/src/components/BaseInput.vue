<template>
  <div class="mb-3">
    <label v-if="label" class="form-label">{{ label }}</label>
    <input
      :type="type"
      :placeholder="placeholder"
      class="form-control form-control-lg rounded-3"
      :value="modelValue"                          
      @input="$emit('update:modelValue', $event.target.value)" />
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  label: String,
  placeholder: String,
  type: {
    type: String,
    default: 'text',
  },
})
defineEmits(['update:modelValue'])              
</script>
