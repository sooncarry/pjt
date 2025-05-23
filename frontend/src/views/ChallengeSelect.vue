<template>
  <div class="select-page">
    <h2>🔥 여러 챌린지를 선택해 시작해보세요</h2>
    <div class="template-list">
      <div
        v-for="tpl in templates"
        :key="tpl.id"
        :class="['template-card', {
          selected: selectedIds.includes(tpl.id),
          disabled: activeTemplateIds.includes(tpl.id)
        }]"
        @click="!activeTemplateIds.includes(tpl.id) && toggleSelect(tpl.id)"
      >
        <h3>{{ tpl.name }}</h3>
        <p>{{ tpl.description }}</p>
        <p v-if="activeTemplateIds.includes(tpl.id)" class="badge">진행중</p>
      </div>
    </div>
    <button class="start-btn" @click="startChallenges" :disabled="selectedIds.length === 0">
      선택한 챌린지 시작하기 ({{ selectedIds.length }})
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const templates = ref([])
const selectedIds = ref([])
const activeTemplateIds = ref([])

onMounted(async () => {
  const res1 = await axios.get('/api/savings/templates/')
  templates.value = res1.data

  const res2 = await axios.get('/api/savings/active/')
  activeTemplateIds.value = res2.data.map(ch => ch.template)
})

const toggleSelect = (id) => {
  if (selectedIds.value.includes(id)) {
    selectedIds.value = selectedIds.value.filter(i => i !== id)
  } else {
    selectedIds.value.push(id)
  }
}

const startChallenges = async () => {
  for (const id of selectedIds.value) {
    const tpl = templates.value.find(t => t.id === id)
    await axios.post('/api/savings/start/', {
      template: tpl.id,
      goal_amount: tpl.default_goal_amount,
      total_units: tpl.default_total_units,
      unit: tpl.default_unit
    })
  }
  router.push('/saving/challenges')
}
</script>

<style scoped>
.select-page {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}
.template-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}
.template-card {
  border: 2px solid #ddd;
  padding: 1rem;
  width: 220px;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;
  background-color: white;
}
.template-card.selected {
  border-color: #4caf50;
  background-color: #f0fff0;
}
.template-card.disabled {
  opacity: 0.6;
  pointer-events: none;
}
.badge {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: white;
  background-color: #f44336;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
}
.start-btn {
  margin-top: 2rem;
  background-color: #4caf50;
  color: white;
  font-size: 1rem;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
.start-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
