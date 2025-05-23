<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import { onMounted, ref } from 'vue'
import axios from 'axios'

const router = useRouter()
const auth = useAuthStore()
const activeChallenges = ref([])

const goToChallenge = async () => {
  if (!auth.isLoggedIn) {
    alert('챌린지를 시작하려면 로그인해야 합니다.')
    router.push('/login')
  } else {
    try {
      const res = await axios.get('/api/savings/active/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      if (res.data.length === 0) {
        router.push('/saving/challenges/select')  // 챌린지가 없으면 선택창으로 이동
      } else {
        router.push('/saving/challenges')  // 있으면 디테일로
      }
    } catch (err) {
      router.push('/saving/challenges/select')  // 요청 실패 시에도 선택 페이지로 fallback
    }
  }
}


const goToRecommend = () => {
  if (!auth.isLoggedIn) {
    alert('예적금 추천은 로그인 후 이용할 수 있습니다.')
    router.push('/login')
  } else {
    router.push('/saving/recommend')
  }
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
  <div class="saving-main">
    <h1>💸 매일 한 걸음씩, 더 나은 금융 습관!</h1>
    <p class="subtext">
      오늘부터 나만의 저축 챌린지를 시작하고,<br />
      당신의 금융 습관을 멋지게 바꿔보세요.
    </p>

    <div class="button-group">
      <button class="btn-main" @click="goToChallenge">
        {{ activeChallenges.length > 0 ? '진행 중인 챌린지 보기' : '챌린지 진행하기' }}
      </button>
      <button class="btn-sub" @click="goToRecommend">
        예적금 추천받기
      </button>
    </div>
  </div>
</template>

<style scoped>
.saving-main {
  max-width: 700px;
  margin: 0 auto;
  padding: 3rem 2rem;
  text-align: center;
}
.subtext {
  margin: 1.5rem 0;
  font-size: 1.25rem;
}
.button-group {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}
.btn-main, .btn-sub {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
}
.btn-main {
  background-color: #4caf50;
  color: white;
}
.btn-sub {
  background-color: #2196f3;
  color: white;
}
</style>
