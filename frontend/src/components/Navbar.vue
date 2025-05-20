<template>
  <nav class="navbar">
    <div class="nav-left">
      <router-link to="/">홈</router-link>
      <router-link to="/deposit">예금</router-link>
      <router-link to="/stock">주식</router-link>
      <router-link to="/education">금융 교육</router-link>
      <router-link to="/saving">저축</router-link>
      <router-link to="/community">커뮤니티</router-link>
    </div>

    <div class="nav-right">
      <template v-if="isLoggedIn">
        <router-link to="/mypage">마이페이지</router-link>
        <button @click="logout">로그아웃</button>
      </template>
      <template v-else>
        <router-link to="/login">로그인</router-link>
        <router-link to="/signup">회원가입</router-link>
      </template>
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

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.nav-left,
.nav-right {
  display: flex;
  gap: 1.2rem;
  align-items: center;
}

a {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
}

button {
  background: transparent;
  border: none;
  font-weight: bold;
  color: #007bff;
  cursor: pointer;
}
</style>
