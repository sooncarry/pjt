// stores/challenge.js
import { defineStore } from 'pinia'

export const useChallengeStore = defineStore('challenge', {
  state: () => ({
    activeChallenge: null, // 현재 진행 중인 챌린지 ID or 전체 객체
  }),
  actions: {
    startChallenge(challenge) {
      this.activeChallenge = challenge
      localStorage.setItem('activeChallenge', JSON.stringify(challenge))
    },
    loadChallenge() {
      const saved = localStorage.getItem('activeChallenge')
      if (saved) {
        this.activeChallenge = JSON.parse(saved)
      }
    },
    endChallenge() {
      this.activeChallenge = null
      localStorage.removeItem('activeChallenge')
    }
  },
})
