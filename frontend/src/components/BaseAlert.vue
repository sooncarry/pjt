<script setup>
import { computed } from 'vue'

// props 정의
const props = defineProps({
  type: { type: String, default: 'info' },
  title: String,
  message: String,
  closable: Boolean,
})

// 이벤트 정의
defineEmits(['close'])

// ✅ props.type처럼 접근해야 함!
const iconClass = computed(() => {
  switch (props.type) {
    case 'success': return 'bi bi-check-circle text-success'
    case 'danger': return 'bi bi-x-circle text-danger'
    case 'warning': return 'bi bi-exclamation-triangle text-warning'
    default: return 'bi bi-info-circle text-primary'
  }
})

const alertClass = computed(() => {
  return {
    'border-success bg-white': props.type === 'success',
    'border-danger bg-white': props.type === 'danger',
    'border-warning bg-white': props.type === 'warning',
    'border-primary bg-white': props.type === 'info',
  }
})
</script>
