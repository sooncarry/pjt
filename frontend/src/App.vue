<template>
  <div id="app">
    <!-- ✅ 인트로 애니메이션 -->
    <Intro v-if="!introDone" @finished="introDone = true" />

    <!-- ✅ 인트로가 끝난 후 실제 앱 화면 렌더링 -->
    <template v-else>
      <Navbar />
      <BaseAlert
        v-if="alertMsg"
        :message="alertMsg"
        :type="alertType"
        class="fixed-top mt-3 mx-auto"
        style="max-width: 500px; z-index: 1050;"
      />
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'

import Navbar from './components/Navbar.vue'
import BaseAlert from '@/components/BaseAlert.vue'
import Intro from '@/components/Intro.vue' // ✅ 새로 만든 컴포넌트

// ✅ 전역 상태
const alertMsg = ref('')
const alertType = ref('success')
const introDone = ref(false) // ✅ 인트로 종료 여부

// 전역으로 제공
provide('alertMsg', alertMsg)
provide('alertType', alertType)
</script>
