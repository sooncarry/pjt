<template>
  <div id="app">
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
import Navbar from './components/Navbar.vue'
import { ref, provide } from 'vue'
import BaseAlert from '@/components/BaseAlert.vue'

// ✅ 전역 상태 제공
const alertMsg = ref('')
const alertType = ref('success')

// 전역으로 내보냄
provide('alertMsg', alertMsg)
provide('alertType', alertType)
</script>
