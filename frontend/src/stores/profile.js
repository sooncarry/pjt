// src/stores/profile.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useProfileStore = defineStore('profile', () => {
  const title = ref(null)
  const savingStyle = ref(null)
  const spendingStyle = ref(null)
  const checklistSubmitted = ref(false)

  // 서버에서 재무 프로필 불러오기
  const fetchProfile = async () => {
    try {
      const res = await axios.get('/api/financial-profile/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      const data = res.data
      title.value = data.title
      savingStyle.value = data.saving_style
      spendingStyle.value = data.spending_style
      checklistSubmitted.value = data.checklist_submitted
    } catch (err) {
      console.error('재무 성향 가져오기 실패:', err)
    }
  }

  return {
    title,
    savingStyle,
    spendingStyle,
    checklistSubmitted,
    fetchProfile,
  }
})
