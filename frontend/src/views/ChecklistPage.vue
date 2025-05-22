<template>
  <div>
    <h2>재무 성향 체크리스트</h2>
    <form @submit.prevent="submitChecklist">
      <div v-for="(question, i) in questions" :key="i">
        <p>{{ question.text }}</p>
        <div v-for="(choice, j) in question.choices" :key="j">
          <label>
            <input type="radio" :name="'q' + i" :value="choice.score" v-model="answers[i]" required>
            {{ choice.text }}
          </label>
        </div>
      </div>
      <button type="submit">성향 진단하기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useProfileStore } from '@/stores/profile'

const profileStore = useProfileStore()


const router = useRouter()


const questions = [
  { text: '비정기 소비 비율은?', choices: [
    { text: '10% 이하', score: 0 },
    { text: '10~30%', score: 1 },
    { text: '30% 이상', score: 2 },
  ]},
  { text: '충동구매 빈도는?', choices: [
    { text: '거의 없음', score: 0 },
    { text: '가끔 있음', score: 1 },
    { text: '자주 함', score: 2 },
  ]},
  { text: '저축 상품 선호는?', choices: [
    { text: '예적금', score: 0 },
    { text: '펀드/보험', score: 1 },
    { text: '주식/코인', score: 2 },
  ]},
  { text: '월 저축 비율은?', choices: [
    { text: '10% 이하', score: 0 },
    { text: '10~30%', score: 1 },
    { text: '30% 이상', score: 2 },
  ]},
  { text: '저축 계획 유형은?', choices: [
    { text: '단기 목적 위주', score: 0 },
    { text: '균형 계획', score: 1 },
    { text: '조기 자산 형성', score: 2 },
  ]},
]

const answers = ref(new Array(questions.length).fill(null))

const submitChecklist = async () => {
  const spending_score = answers.value.slice(0, 2).reduce((a, b) => a + Number(b), 0)
  const saving_score = answers.value.slice(2).reduce((a, b) => a + Number(b), 0)

  const res = await axios.post('/api/financial-profile/', {
    spending_score,
    saving_score,
  }, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  console.log('제출')
  await profileStore.fetchProfile()
  alert(`'${profileStore.title}'님, 환영합니다! 우리 부자됩시다 💰`)
  router.push('/mypage')
}

</script>
