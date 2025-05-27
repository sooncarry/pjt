<template>
  <nav class="navbar navbar-light bg-white border-bottom shadow-sm py-3">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- 왼쪽 네비게이션 -->
      <div class="d-flex gap-1">
        <RouterLink to="/" class="nav-link fw-bold custom-nav-link px-3">
          <img src="@/assets/logo_tiggle.png" alt="Tiggle 로고" style="height: 22px;" />
        </RouterLink>
        <RouterLink to="/finance" class="nav-link fw-semibold custom-nav-link">금융</RouterLink>
        <RouterLink to="/stock" class="nav-link fw-semibold custom-nav-link">주식</RouterLink>
        <RouterLink to="/education" class="nav-link fw-semibold custom-nav-link">지식</RouterLink>
        <RouterLink to="/saving" class="nav-link fw-semibold custom-nav-link">저축</RouterLink>
        <RouterLink to="/community" class="nav-link fw-semibold custom-nav-link">커뮤니티</RouterLink>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const hover = ref(false)

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

<style scoped>
.btn {
  font-size: 1.025rem;
}

.custom-nav-link {
  color: #5A45FF;
  transition: background-color 0.3s, color 0.3s;
  border-radius: 1.5rem;
  padding: 0.4rem 1rem;
}

.custom-nav-link:hover {
  background-color: #5A45FF;
  color: white;
  text-decoration: none;
}

</style>