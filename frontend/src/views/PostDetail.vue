<template>
  <!-- 상단 네비게이션(NAVBAR) 아래 여백 추가 -->
  <div class="container my-5" style="padding-top: 80px;">
    <div class="row">
      <!-- 사이드바 -->
      <div class="col-md-3 mb-4">
        <div class="card shadow-sm border-0 rounded-4 p-3">
          <h5 class="fw-bold mb-3">커뮤니티 주제</h5>
          <ul class="list-unstyled">
            <li class="mb-2">
              <router-link
                to="/community"
                class="text-decoration-none"
                :class="{
                  'fw-bold text-primary': !post?.category,
                  'text-dark': post?.category
                }"
              >
                전체글
              </router-link>
            </li>
            <li
              v-for="(name, key) in categoryDisplayName"
              :key="key"
              class="mb-2"
            >
              <router-link
                :to="`/community/category/${key}`"
                class="text-decoration-none"
                :class="{
                  'fw-bold text-primary': post?.category === key,
                  'text-dark': post?.category !== key
                }"
              >
                {{ name }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>

      <!-- 상세 콘텐츠 -->
      <div class="col-md-9">
        <!-- 뒤로가기 -->
        <button
          @click="goBack"
          class="btn btn-outline-secondary btn-sm mb-3"
        >
          ← 뒤로가기
        </button>

        <div v-if="post" class="card p-4 shadow-sm border-0 rounded-4">
          <h2 class="h4 fw-bold">{{ post.title }}</h2>
          <p class="text-muted small">작성자: {{ post.author_username }}</p>
          <p class="mt-3" style="white-space: pre-line;">{{ post.content }}</p>

          <!-- 수정/삭제 -->
          <div
            v-if="isLoggedIn && isMine(post.author_username)"
            class="d-flex gap-2 justify-content-end mt-3"
          >
            <button
              class="btn btn-outline-secondary btn-sm rounded-pill"
              @click="goEdit"
            >
              수정
            </button>
            <button
              class="btn btn-outline-danger btn-sm rounded-pill"
              @click="deletePost"
            >
              삭제
            </button>
          </div>

          <!-- 좋아요 -->
          <div class="like-section mt-4 d-flex align-items-center gap-2">
            <button
              @click="toggleLike"
              :disabled="!isLoggedIn"
              class="heart-button"
            >
              <span v-if="liked">❤️</span>
              <span v-else>🤍</span>
            </button>
            <span class="text-muted small">{{ likesCount }}명이 좋아합니다</span>
          </div>

          <!-- 댓글 -->
          <div class="mt-5">
            <h5 class="fw-semibold mb-3">💬 댓글</h5>

            <div v-if="post.comments?.length">
              <div
                v-for="comment in post.comments"
                :key="comment.id"
                class="mb-3 p-3 bg-light rounded-3 position-relative"
              >
                <!-- 삭제용 X 아이콘 -->
                <span
                  v-if="isLoggedIn && isMine(comment.author_username)"
                  class="position-absolute top-0 end-0 m-2"
                  style="cursor: pointer; color: #dc3545; font-size: 1.2rem;"
                  @click="deleteComment(comment.id)"
                >
                  ×
                </span>

                <p class="mb-1">
                  <strong>{{ comment.author_username }}</strong>:
                  <span>{{ comment.content }}</span>
                </p>
              </div>
            </div>
            <div v-else class="text-muted">댓글이 없습니다.</div>

            <div class="mt-4">
              <h6 class="fw-bold">✏️ 댓글 작성</h6>
              <div v-if="isLoggedIn">
                <CommentForm @submit="(content) => submitComment(null, content)" />
              </div>
              <div v-else class="text-muted small">
                댓글을 작성하시려면 로그인 해주세요.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div><!-- /.container -->
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
const isLoggedIn = !!localStorage.getItem('access_token')
const liked = ref(false)
const likesCount = ref(0)

// 사이드바 카테고리 이름 매핑
const categoryDisplayName = {
  stock: '주식방',
  deposit: '예적금방',
  saving: '저축방',
  free: '자유이야기방',
  worker: '직장인방'
}

// 뒤로가기
const goBack = () => {
  router.back()
}

// 게시글 로드
onMounted(async () => {
  try {
    const res = await axios.get(`/api/boards/${route.params.id}/`)
    post.value = res.data
    liked.value = post.value.likes?.includes(currentUsername)
    likesCount.value = post.value.likes_count
  } catch (err) {
    console.error('게시글 조회 실패:', err)
  }
})

const isMine = author => author === currentUsername

const goEdit = () => {
  router.push({ name: 'PostEdit', params: { id: route.params.id } })
}

const deletePost = async () => {
  if (confirm('정말 삭제하시겠습니까?')) {
    await axios.delete(`/api/boards/${route.params.id}/`)
    goBack()
  }
}

const submitComment = async (parentId, content) => {
  if (!content.trim()) return
  await axios.post('/api/boards/comments/', {
    post: post.value.id,
    content,
    parent: parentId
  })
  const updated = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = updated.data
}

const deleteComment = async id => {
  if (!confirm('해당 댓글을 삭제하시겠습니까?')) return
  await axios.delete(`/api/boards/comments/${id}/`)
  const updated = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = updated.data
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
