<template>
  <div>
    <h1>{{ isEdit ? '게시글 수정' : '게시글 작성' }}</h1>
    <form @submit.prevent="handleSubmit">
      <input v-model="form.title" placeholder="제목" />
      <textarea v-model="form.content" placeholder="내용"></textarea>
      <select v-model="form.category" required>
        <option value="" disabled>카테고리 선택</option>
        <option value="stock">주식방</option>
        <option value="deposit">예적금방</option>
        <option value="saving">저축방</option>
        <option value="free">자유이야기방</option>
        <option value="worker">직장인방</option>
      </select>
      <button type="submit">{{ isEdit ? '수정' : '작성' }}</button>
    </form>
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
    // console.log('access_token:', localStorage.getItem('access_token'))
    // console.log('axios Authorization header:', axios.defaults.headers.common['Authorization'])

  if (isEdit) {
    await axios.put(`/api/boards/${route.params.id}/`, form.value)
  } else {
    await axios.post('/api/boards/', form.value)
  }
  router.push('/community')
}
</script>
