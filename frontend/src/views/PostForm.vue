<template>
  <div class="container my-5">
    <div class="card p-4 shadow-sm border-0 rounded-4">
      <h1 class="h5 fw-bold mb-4">{{ isEdit ? '게시글 수정' : '게시글 작성' }}</h1>

      <form @submit.prevent="handleSubmit" class="d-flex flex-column gap-3">
        <select
          v-model="form.category"
          class="form-select form-select-sm rounded-3"
          required
        >
          <option value="" disabled>카테고리 선택</option>
          <option value="stock">주식방</option>
          <option value="deposit">예적금방</option>
          <option value="saving">저축방</option>
          <option value="free">자유이야기방</option>
          <option value="worker">직장인방</option>
        </select>
        <input
          v-model="form.title"
          placeholder="제목을 입력하세요"
          class="form-control form-control-sm rounded-3"
          required
        />
        
        <textarea
          v-model="form.content"
          placeholder="내용을 입력하세요"
          class="form-control form-control-sm rounded-3"
          rows="6"
          required
        ></textarea>

        

        <button type="submit" class="btn btn-primary btn-sm rounded-pill align-self-end px-4">
          {{ isEdit ? '수정' : '작성' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

const isEdit = route.name === 'PostEdit'

const form = ref({
  title: '',
  content: '',
  category: route.query.category || '',
})

onMounted(async () => {
  if (isEdit) {
    const res = await axios.get(`/api/boards/${route.params.id}/`)
    form.value = { ...res.data }
  }
})

const handleSubmit = async () => {
  if (isEdit) {
    await axios.put(`/api/boards/${route.params.id}/`, form.value)
  } else {
    await axios.post('/api/boards/', form.value)
  }
  router.push('/community')
}
</script>

<style scoped>
/* 필요 시 추가 */
</style>
