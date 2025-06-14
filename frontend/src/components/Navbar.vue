<template>
  <nav class="navbar fixed-top border-bottom shadow-sm py-3">
    <div class="container d-flex justify-content-between align-items-center">
      <!-- 왼쪽 네비게이션 -->
      <div class="d-flex gap-1">
        <RouterLink
          to="/"
          class="nav-link fw-bold custom-nav-link px-3 logo-wrapper"
          @mouseenter="toggleLogo(true)"
          @mouseleave="toggleLogo(false)"
        >
          <img
            :src="logoSrc"
            alt="Tiggle 로고"
            class="logo-img"
          />
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
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const logoDefault = new URL('@/assets/logo_tiggle.png', import.meta.url).href
const logoWhite = new URL('@/assets/logo_tiggle_white.png', import.meta.url).href

const logoSrc = ref(logoDefault)

const router = useRouter()
const isLoggedIn = computed(() => !!localStorage.getItem('access_token'))

const toggleLogo = (hovering) => {
  logoSrc.value = hovering ? logoWhite : logoDefault
}

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/login')
  window.location.reload()
}
</script>

<style scoped>
.navbar.fixed-top {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1030;
  background-color: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(10px);
}

.btn {
  font-size: 1.025rem;
}

.custom-nav-link {
  color: #5A45FF;
  transition: background-color 0.3s, color 0.3s;
  border-radius: 1.5rem;
  padding: 0.4rem 1rem;
}

/* active 상태에서도 기본 색상을 유지하도록 override */
.custom-nav-link.router-link-active,
.custom-nav-link.active {
  color: #5A45FF !important;
  background-color: transparent !important;
}

.custom-nav-link:hover {
  background-color: #5A45FF;
  color: white;
  text-decoration: none;
}

.logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  width: auto;
  border-radius: 1.5rem;
  transition: background-color 0.3s ease;
}

.logo-img {
  height: 22px;
  transition: filter 0.3s ease;
}

.logo-wrapper:hover {
  background-color: #5A45FF;
}

.logo-wrapper:hover .logo-img {
  filter: brightness(10);
}
</style>
