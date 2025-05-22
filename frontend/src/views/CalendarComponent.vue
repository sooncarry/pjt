<template>
  <div class="calendar">
    <h3>{{ currentYear }}년 {{ currentMonth + 1 }}월</h3>
    <div class="weekdays">
      <div v-for="day in ['일','월','화','수','목','금','토']" :key="day">{{ day }}</div>
    </div>
    <div class="dates">
      <div v-for="n in firstDay" :key="'empty-' + n" class="empty"></div>
      <div
        v-for="day in daysInMonth"
        :key="day"
        class="date-cell"
        :class="{ checked: isChecked(day) }"
        @click="check(day)"
      >
        {{ day }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

// props: 전달받은 체크 정보
const props = defineProps({
  checks: Array, // ex: [{ date: '2025-05-21', is_saved: true }, ...]
})

const emit = defineEmits(['check'])

const today = new Date()
const currentYear = today.getFullYear()
const currentMonth = today.getMonth()

const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate()
const firstDay = new Date(currentYear, currentMonth, 1).getDay()

// 날짜가 체크된 날짜인지 판단
const isChecked = (day) => {
  const dayStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  return props.checks?.some(c => c.date === dayStr && c.is_saved)
}

// 클릭 시 부모에 알림
const check = (day) => {
  const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
  emit('check', dateStr)
}
</script>

<style scoped>
.calendar {
  margin: 2rem 0;
}
.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.dates {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.3rem;
}
.empty {
  height: 2rem;
}
.date-cell {
  padding: 0.5rem 0;
  border-radius: 6px;
  background-color: #f2f2f2;
  text-align: center;
  cursor: pointer;
}
.date-cell.checked {
  background-color: #4caf50;
  color: white;
  font-weight: bold;
}
</style>
