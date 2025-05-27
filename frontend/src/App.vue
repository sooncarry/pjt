<template>
  <div id="app">
    <!-- ✅ 인트로 애니메이션 -->
      <Navbar />
      <BaseAlert
        v-if="alertMsg"
        :message="alertMsg"
        :type="alertType"
        class="fixed-top mt-3 mx-auto"
        style="max-width: 500px; z-index: 1050;"
      />
      <router-view />
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'

import Navbar from './components/Navbar.vue'
import BaseAlert from '@/components/BaseAlert.vue'


// ✅ 전역 상태
const alertMsg = ref('')
const alertType = ref('success')
const introDone = ref(false) // ✅ 인트로 종료 여부

// 전역으로 제공
provide('alertMsg', alertMsg)
provide('alertType', alertType)
</script>
