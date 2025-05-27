<template>
  <div v-if="post" class="container my-5">
    <div class="card p-4 shadow-sm border-0 rounded-4">
      <h2 class="h4 fw-bold">{{ post.title }}</h2>
      <p class="text-muted small">작성자: {{ post.author_username }}</p>
      <p class="mt-3" style="white-space: pre-line;">{{ post.content }}</p>

      <!-- 수정/삭제 버튼 -->
      <div
        v-if="isLoggedIn && isMine(post.author_username)"
        class="d-flex gap-2 justify-content-end mt-3"
      >
        <button class="btn btn-outline-secondary btn-sm rounded-pill" @click="goEdit">수정</button>
        <button class="btn btn-outline-danger btn-sm rounded-pill" @click="deletePost">삭제</button>
      </div>

      <!-- 좋아요 -->
      <div class="like-section mt-4 d-flex align-items-center gap-2">
        <button @click="toggleLike" :disabled="!isLoggedIn" class="heart-button">
          <span v-if="liked">❤️</span>
          <span v-else>🤍</span>
        </button>
        <span class="text-muted small">{{ likesCount }}명이 좋아합니다</span>
      </div>

      <!-- 댓글 -->
      <div class="mt-5">
        <h5 class="fw-semibold mb-3">💬 댓글</h5>

        <!-- 댓글 리스트 -->
        <div v-if="post.comments && post.comments.length">
          <div
            v-for="comment in post.comments"
            :key="comment.id"
            class="mb-3 p-3 bg-light rounded-3"
          >
            <p class="mb-1">
              <strong>{{ comment.author_username }}</strong>:
              <span>{{ comment.content }}</span>
            </p>
            <button
              v-if="isLoggedIn && isMine(comment.author_username)"
              class="btn btn-sm btn-outline-danger btn-xs rounded-pill mt-2"
              @click="deleteComment(comment.id)"
            >
              삭제
            </button>
          </div>
        </div>
        <div v-else class="text-muted">댓글이 없습니다.</div>

        <!-- 댓글 작성 -->
        <div class="mt-4">
          <h6 class="fw-bold">✏️ 댓글 작성</h6>
          <div v-if="isLoggedIn">
            <CommentForm @submit="(content) => submitComment(null, content)" />
          </div>
          <div v-else class="text-muted small">댓글을 작성하시려면 로그인 해주세요.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
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

// ✅ GET 요청 시 인증 헤더 제거
onMounted(async () => {
  try {
    const res = await axios.get(`/api/boards/${route.params.id}/`, {
      headers: { Authorization: undefined }
    })
    post.value = res.data
    liked.value = post.value.likes?.includes(currentUsername)
    likesCount.value = post.value.likes_count
  } catch (err) {
    console.error('❌ 게시글 상세 요청 실패:', err)
  }
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
  const updated = await axios.get(`/api/boards/${route.params.id}/`, {
    headers: { Authorization: undefined }
  })
  post.value = updated.data
}

const deleteComment = async (id) => {
  if (confirm('댓글을 삭제할까요?')) {
    await axios.delete(`/api/boards/comments/${id}/`)
    const updated = await axios.get(`/api/boards/${route.params.id}/`, {
      headers: { Authorization: undefined }
    })
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
</style>
