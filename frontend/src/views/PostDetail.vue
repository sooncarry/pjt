<template>
  <div v-if="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>

    <!-- 수정/삭제 버튼 (작성자만 보임) -->
    <div v-if="isMine(post.author_username)">
      <button @click="goToEditPage">수정</button>
      <button @click="deletePost">삭제</button>
    </div>

    <!-- 댓글 목록 -->
    <h3>댓글</h3>
    <div v-for="comment in post.comments" :key="comment.id" class="comment">
      <p>
        <strong>{{ comment.author_username }}</strong>: {{ comment.content }}
      </p>
      <div v-if="comment.id === editingCommentId">
        <CommentForm
          :content="comment.content"
          :isEdit="true"
          @submit="updateComment(comment.id)"
          @cancel="editingCommentId = null"
        />
      </div>
      <div v-else>
        <button v-if="isMine(comment.author_username)" @click="startEdit(comment.id, comment.content)">수정</button>
        <button v-if="isMine(comment.author_username)" @click="deleteComment(comment.id)">삭제</button>
        <button @click="toggleReply(comment.id)">답글</button>
      </div>

      <!-- 대댓글 -->
      <div class="reply" v-for="reply in comment.replies" :key="reply.id">
        <p>
          ↳ <strong>{{ reply.author_username }}</strong>: {{ reply.content }}
        </p>
        <div v-if="reply.id === editingCommentId">
          <CommentForm
            :content="reply.content"
            :isEdit="true"
            @submit="updateComment(reply.id)"
            @cancel="editingCommentId = null"
          />
        </div>
        <div v-else>
          <button v-if="isMine(reply.author_username)" @click="startEdit(reply.id, reply.content)">수정</button>
          <button v-if="isMine(reply.author_username)" @click="deleteComment(reply.id)">삭제</button>
        </div>
      </div>

      <!-- 대댓글 입력창 -->
      <div v-if="replyTargetId === comment.id">
        <CommentForm @submit="submitComment(comment.id)" />
      </div>
    </div>

    <!-- 일반 댓글 작성 -->
    <h4>댓글 작성</h4>
    <CommentForm @submit="submitComment(null)" />
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
const newComment = ref('')
const editingCommentId = ref(null)
const editingContent = ref('')
const replyTargetId = ref(null)

const currentUsername = localStorage.getItem('username')

onMounted(async () => {
  const res = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = res.data
})

const isMine = (author) => author === currentUsername

const submitComment = async (parentId = null, content = null) => {
  await axios.post('/api/boards/comments/', {
    post: post.value.id,
    content: content || newComment.value,
    parent: parentId
  })
  const updated = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = updated.data
  newComment.value = ''
  replyTargetId.value = null
}

const startEdit = (id, content) => {
  editingCommentId.value = id
  editingContent.value = content
}

const updateComment = (id) => async (newContent) => {
  await axios.put(`/api/boards/comments/${id}/`, { content: newContent })
  const updated = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = updated.data
  editingCommentId.value = null
}

const deleteComment = async (id) => {
  await axios.delete(`/api/boards/comments/${id}/`)
  const updated = await axios.get(`/api/boards/${route.params.id}/`)
  post.value = updated.data
}

const toggleReply = (commentId) => {
  replyTargetId.value = replyTargetId.value === commentId ? null : commentId
}

// 게시글 수정/삭제용 함수
const goToEditPage = () => {
  router.push(`/community/edit/${post.value.id}`)
}

const deletePost = async () => {
  const confirmed = confirm('정말 삭제하시겠습니까?')
  if (!confirmed) return
  await axios.delete(`/api/boards/${post.value.id}/`)
  alert('삭제 완료')
  router.push('/community')
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
</style>
