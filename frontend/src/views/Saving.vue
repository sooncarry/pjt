<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { onMounted, ref } from 'vue'
import axios from 'axios'
import BaseAlert from '@/components/BaseAlert.vue'

const router = useRouter()
const auth = useAuthStore()
const activeChallenges = ref([])

const alertMsg = ref('')
const alertType = ref('success')

const goToChallenge = async () => {
  if (!auth.isLoggedIn) {
    alertMsg.value = '🚫 챌린지를 시작하려면 로그인해야 합니다.'
    alertType.value = 'danger'
    setTimeout(() => router.push('/login'), 2000)
    return
  }

  try {
    const res = await axios.get('/api/savings/active/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    if (res.data.length === 0) {
      router.push('/saving/challenges/select')
    } else {
      router.push('/saving/challenges')
    }
  } catch (err) {
    router.push('/saving/challenges/select')
  }
}


const goToRecommend = () => {
  if (!auth.isLoggedIn) {
    alertMsg.value = '🔐 예적금 추천은 로그인 후 이용할 수 있습니다.'
    alertType.value = 'danger'
    setTimeout(() => router.push('/login'), 2000)
    return
  }

  router.push('/saving/recommend')
}

onMounted(async () => {
  if (auth.isLoggedIn) {
    try {
      const res = await axios.get('/api/savings/active/')
      activeChallenges.value = res.data
    } catch (err) {
      activeChallenges.value = []
    }
  }
})
</script>

<template>
  <BaseAlert v-if="alertMsg" :message="alertMsg" :type="alertType" />
  
  <div class="container my-5 text-center">
    <h1 class="h3 fw-bold mb-3">💸 매일 한 걸음씩, 더 나은 금융 습관!</h1>
    <p class="text-muted fs-6 mb-4">
      오늘부터 나만의 저축 챌린지를 시작하고,<br />
      당신의 금융 습관을 멋지게 바꿔보세요.
    </p>

    <div class="d-flex justify-content-center gap-3 flex-wrap">
      <button class="btn btn-success btn-lg rounded-pill px-4"
              @click="goToChallenge">
        {{ activeChallenges.length > 0 ? '진행 중인 챌린지 보기' : '챌린지 진행하기' }}
      </button>
      <button class="btn btn-primary btn-lg rounded-pill px-4"
              @click="goToRecommend">
        예적금 추천받기
      </button>
    </div>
  </div>
</template>

<style scoped>
/* 추가 커스텀 스타일이 필요한 경우만 작성 가능 */
</style>
