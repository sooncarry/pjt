<template>
  <nav class="navbar navbar-light bg-white border-bottom shadow-sm py-3">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- 왼쪽 네비게이션 -->
      <div class="d-flex gap-4">
        <RouterLink to="/" class="nav-link fw-semibold text-primary">홈</RouterLink>
        <RouterLink to="/finance" class="nav-link fw-semibold text-primary">금융</RouterLink>
        <RouterLink to="/stock" class="nav-link fw-semibold text-primary">주식</RouterLink>
        <RouterLink to="/education" class="nav-link fw-semibold text-primary">금융 교육</RouterLink>
        <RouterLink to="/saving" class="nav-link fw-semibold text-primary">저축</RouterLink>
        <RouterLink to="/community" class="nav-link fw-semibold text-primary">커뮤니티</RouterLink>
      </div>

      <!-- 오른쪽 로그인/로그아웃 -->
      <div class="d-flex gap-3 align-items-center">
        <template v-if="isLoggedIn">
          <RouterLink to="/mypage" class="btn btn-outline-primary btn-sm rounded-pill px-2">마이페이지</RouterLink>
          <button class="btn btn-primary btn-sm rounded-pill px-2" @click="logout">로그아웃</button>
        </template>
        <template v-else>
          <RouterLink to="/login" class="btn btn-outline-primary btn-sm rounded-pill px-2">로그인</RouterLink>
          <RouterLink to="/signup" class="btn btn-primary btn-sm rounded-pill px-2">회원가입</RouterLink>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token')
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
  window.location.reload()
}
</script>
