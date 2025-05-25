<template>
  <div class="calendar container my-4">
    <h3 class="h5 fw-bold mb-3 text-center">{{ currentYear }}년 {{ currentMonth + 1 }}월</h3>

    <div class="weekdays">
      <div v-for="day in ['일','월','화','수','목','금','토']" :key="day" class="text-muted small fw-semibold text-center">
        {{ day }}
      </div>
    </div>

    <div class="dates">
      <div v-for="n in firstDay" :key="'empty-' + n" class="empty"></div>

      <div
        v-for="day in daysInMonth"
        :key="day"
        class="date-cell text-center small"
        :class="{ checked: isChecked(day) }"
        @click="check(day)"
      >
        {{ day }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  checks: Array, // ex: [{ date: '2025-05-21', is_saved: true }]
})

const emit = defineEmits(['check'])

const today = new Date()
const currentYear = today.getFullYear()
const currentMonth = today.getMonth()

const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
const firstDay = new Date(currentYear, currentMonth, 1).getDay()

const isChecked = (day) => {
  const dayStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  return props.checks?.some(c => c.date === dayStr && c.is_saved)
}

const check = (day) => {
  const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  emit('check', dateStr)
}
</script>

<style scoped>
.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  margin-bottom: 0.5rem;
}
.dates {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.4rem;
}
.empty {
  height: 2.2rem;
}
.date-cell {
  padding: 0.55rem 0;
  border-radius: 0.5rem;
  background-color: #f8f9fa;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.date-cell:hover {
  background-color: #e9ecef;
}
.date-cell.checked {
  background-color: #198754;
  color: white;
  font-weight: bold;
}
</style>
