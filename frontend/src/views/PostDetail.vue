<template>
  <div v-if="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.author_username }}</p>
    <p>{{ post.content }}</p>

    <div v-if="isLoggedIn && isMine(post.author_username)">
      <button @click="goEdit">수정</button>
      <button @click="deletePost">삭제</button>
    </div>

    <div class="like-section">
      <button @click="toggleLike" :disabled="!isLoggedIn" class="heart-button">
        <span v-if="liked">❤️</span>
        <span v-else>🤍</span>
      </button>
      <span>{{ likesCount }}명이 좋아합니다</span>
    </div>

    <h3>댓글</h3>
    <div v-if="post.comments && post.comments.length">
      <!-- 기존 댓글 렌더링 부분 안에 추가 -->
      <div v-for="comment in post.comments" :key="comment.id" class="comment">
        <p><strong>{{ comment.author_username }}</strong>: {{ comment.content }}</p>
        <button v-if="isLoggedIn && isMine(comment.author_username)" @click="deleteComment(comment.id)">삭제</button>
      </div>

    </div>
    <div v-else>
      <p>댓글이 없습니다.</p>
    </div>

    <h4>댓글 작성</h4>
    <div v-if="isLoggedIn">
      <CommentForm @submit="(content) => submitComment(null, content)" />
    </div>
    <div v-else>
      <p style="color: gray;">댓글을 작성하시려면 로그인 해주세요.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import CommentForm from '@/components/CommentForm.vue'

const route = useRoute()
const router = useRouter()
const post = ref(null)
const currentUsername = localStorage.getItem('username')
const liked = ref(false)
const likesCount = ref(0)
const isLoggedIn = !!localStorage.getItem('access_token')

onMounted(async () => {
  const res = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = res.data
  console.log('작성자:', post.value.author_username)
  console.log('현재 사용자:', currentUsername)

  liked.value = post.value.likes?.includes(currentUsername)  // 서버 응답에 포함되는 경우
  likesCount.value = post.value.likes_count
})

const isMine = (author) => author === currentUsername

const goEdit = () => router.push(`/community/${route.params.id}/edit`)

const deletePost = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await axios.delete(`/api/boards/${route.params.id}/`)
    router.push('/community')
  }
}

const submitComment = async (parentId = null, content = '') => {
  if (!content.trim()) return

  await axios.post('/api/boards/comments/', {
    post: post.value.id,
    content: content,
    parent: parentId
  })

  const updated = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = updated.data
}

const deleteComment = async (id) => {
  if (confirm('댓글을 삭제할까요?')) {
    await axios.delete(`/api/boards/comments/${id}/`)
    const updated = await axios.get(`/api/boards/${route.params.id}/`)
    post.value = updated.data
  }
}

const toggleLike = async () => {
  if (!isLoggedIn) {
    alert('로그인 후 이용 가능합니다.')
    return
  }

  const res = await axios.post(`/api/boards/${route.params.id}/like/`)
  liked.value = res.data.liked
  likesCount.value = res.data.likes_count
}
</script>

<style scoped>
.comment {
  margin-bottom: 1rem;
}
.reply {
  margin-left: 1.5rem;
  font-size: 0.95rem;
  color: #555;
}
.heart-button {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
}
.heart-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
.like-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem 0;
}
</style>