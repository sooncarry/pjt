<!-- src/App.vue -->
<template>
  <div id="app">
    <!-- 네비게이션 -->
    <Navbar />

    <!-- 글로벌 Alert -->
    <BaseAlert
      v-if="alertMsg"
      :message="alertMsg"
      :type="alertType"
      class="fixed-top mt-3 mx-auto"
      style="max-width: 500px; z-index: 1050;"
    />

    <!-- 메인 컨텐츠: margin-top 으로 네비 아래에서 시작 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'

import Navbar from './components/Navbar.vue'
import BaseAlert from '@/components/BaseAlert.vue'

// 전역 알림 메시지 상태
const alertMsg = ref('')
const alertType = ref('success')

// 자식 컴포넌트에 제공
provide('alertMsg', alertMsg)
provide('alertType', alertType)
</script>

<style>
/* 네비 높이에 맞춰 변수 선언 (3.5rem ≒ 56px) */
:root {
  --navbar-height: 3.5rem;
}

/* 네비 높이만큼 메인 컨텐츠를 내려줍니다 */
.main-content {
  margin-top: var(--navbar-height);
}
</style>
