<template>
  <div class="container my-5 text-center"style="padding-top: 120px;">
    <h2 class="h4 fw-bold mb-4">🔥 여러 챌린지를 선택해 시작해보세요</h2>

    <div class="row justify-content-center g-4">
      <div
        class="col-12 col-sm-6 col-md-4 col-lg-3"
        v-for="tpl in templates"
        :key="tpl.id"
      >
        <div
          class="card h-100 shadow-sm rounded-4 p-3 position-relative"
          :class="{
            'border-success bg-light': selectedIds.includes(tpl.id),
            'opacity-50': activeTemplateIds.includes(tpl.id)
          }"
          style="cursor: pointer;"
          @click="!activeTemplateIds.includes(tpl.id) && toggleSelect(tpl.id)"
        >
          <h5 class="fw-semibold">{{ tpl.name }}</h5>
          <p class="text-muted small">{{ tpl.description }}</p>
          <span
            v-if="activeTemplateIds.includes(tpl.id)"
            class="position-absolute top-0 end-0 badge bg-danger m-2"
          >
            진행중
          </span>
        </div>
      </div>
    </div>

    <button
      class="btn btn-success btn-lg rounded-pill px-5 mt-5"
      @click="startChallenges"
      :disabled="selectedIds.length === 0"
    >
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
/* 선택 상태 카드 효과 */
.border-success {
  border: 2px solid #4caf50 !important;
}
/* 비활성 상태는 Bootstrap의 opacity-50로 처리됨 */
</style>
