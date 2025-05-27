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
  } catch {
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
    } catch {
      activeChallenges.value = []
    }
  }
})
</script>

<template>
  <div class="animated-section position-relative text-white py-10">
    <!-- 배경 GIF -->
    <img
      src="@/assets/piggy_loop.png"
      alt="저금통 배경 애니메이션"
      class="bg-gif"
    />

    <!-- 알림 -->
    <BaseAlert v-if="alertMsg" :message="alertMsg" :type="alertType" />

    <!-- 콘텐츠 -->
    <div class="container my-5 text-center position-relative z-1">
      <h1 class="h3 fw-bold mb-3 typing text-dark">
        💸 매일 한 걸음씩, 더 나은 금융 습관!
      </h1>
      <p class="text-muted mb-4 fade-in-text">
        오늘부터 나만의 저축 챌린지를 시작하고,<br />
        당신의 금융 습관을 멋지게 바꿔보세요.
      </p>

      <div class="d-flex justify-content-center gap-3 flex-wrap fade-in-buttons">
        <button
          class="btn btn-success btn-lg rounded-pill px-4"
          @click="goToChallenge"
        >
          {{ activeChallenges.length > 0
            ? '진행 중인 챌린지 보기'
            : '챌린지 진행하기' }}
        </button>
        <button
          class="btn btn-primary btn-lg rounded-pill px-4"
          @click="goToRecommend"
        >
          예적금 추천받기
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animated-section {
  background-color: #f9f7ff;
  overflow: hidden;
  position: relative;
  min-height: 1000px;

  /* ↓ 여기를 margin-top → padding-top 으로 변경 */
  padding-top: var(--navbar-height, 3.5rem);
}

.bg-gif {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-height: 100%;
  object-fit: cover;
  opacity: 0.2;
  z-index: 0;
}

/* 애니메이션 효과 */
.typing {
  display: inline-block;
  overflow: hidden;
  white-space: nowrap;
  border-right: 0.1em solid #5a45ff;
  animation: typing 2s steps(30, end), blink 0.75s step-end infinite;
}
.fade-in-text {
  opacity: 0;
  animation: fadeInUp 1.2s ease-out 0.8s forwards;
}
.fade-in-buttons {
  opacity: 0;
  transform: scale(0.8);
  animation: popIn 1s ease-out 1.8s forwards;
}

/* Keyframes */
@keyframes typing {
  from { width: 0; }
  to   { width: 100%; }
}
@keyframes blink {
  50% { border-color: transparent; }
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
@keyframes popIn {
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
