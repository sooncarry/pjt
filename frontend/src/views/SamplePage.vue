<!-- src/views/SamplePage.vue -->
<template>
  <div class="container mt-5">
    <BaseAlert
      v-if="!hideAlert"
      type="success"
      title="챌린지 완료!"
      message="목표를 성공적으로 달성했어요 🎉"
      :closable="true"
      @close="hideAlert = true"
    />

    <BaseCard class="mt-4">
      <h2 class="h5 fw-semibold mb-2">💰 나의 금융 챌린지</h2>
      <p class="text-muted">저축 습관을 만들고 현명한 금융 생활을 시작해요.</p>

      <BaseInput v-model="name" label="닉네임" placeholder="이름을 입력하세요" />
      <BaseButton>시작하기</BaseButton>
    </BaseCard>
  </div>
</template>

<script setup>
import BaseAlert from '@/components/BaseAlert.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import { ref } from 'vue'

const name = ref('')
const hideAlert = ref(false)
</script>
