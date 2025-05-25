import { createRouter, createWebHistory } from 'vue-router'

// 기본 페이지
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import MyPage from '../views/MyPage.vue'
import ChecklistPage from '@/views/ChecklistPage.vue'
import EmailVerifyHandler from '@/views/EmailVerifyHandler.vue'
import EmailVerified from '@/views/EmailVerified.vue'
import EmailFailed from '@/views/EmailFailed.vue'
import SignupStep2 from '@/views/SignupStep2.vue'



// 주요 기능 페이지
import Finance from '../views/Finance.vue'
import Stock from '../views/Stock.vue'
import Education from '../views/Education.vue'
import Saving from '../views/Saving.vue'
import Community from '../views/Community.vue'

// 커뮤니티 게시판 페이지
import PostDetail from '../views/PostDetail.vue'
import PostForm from '../views/PostForm.vue'

import Tab4ProductRecommend from '@/components/finance/Tab4ProductRecommend.vue'
import StockKnowledge from '@/components/stock/StockKnowledge.vue'
import StockKnowledgeDetail from '@/components/stock/StockKnowledgeDetail.vue'

import SamplePage from '@/views/SamplePage.vue' //디자인 테스트


const routes = [
  // 기본
  { path: '/sample', name: 'SamplePage', component: SamplePage }, //디자인 테스트

  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/mypage', name: 'MyPage', component: MyPage, meta: { requiresAuth: true } },
  { path: '/checklist', name: 'Checklist', component: ChecklistPage },
  { path: '/email-verify/:uidb64/:token', component: EmailVerifyHandler },
  { path: '/email-verified', component: EmailVerified },
  { path: '/email-verify-failed', component: EmailFailed },
  { path: '/signup-step2/:uidb64/:token', component: SignupStep2 },


  // 주요 기능
  { path: '/finance', name: 'Finance', component: Finance },
  { path: '/stock', name: 'Stock', component: Stock },
  { path: '/education', name: 'Education', component: Education },
  { path: '/saving', name: 'Saving', component: Saving },
  { path: '/community', name: 'Community', component: Community },

  // 커뮤니티 게시판
  { path: '/community/:id', name: 'PostDetail', component: PostDetail },
  { path: '/community/create', name: 'PostCreate', component: PostForm },
  { path: '/community/:id/edit', name: 'PostEdit', component: PostForm },
  { path: '/community/category/:category', name: 'CommunityCategory', component: Community },

  // 저축 챌린지 관련
  {
    path: '/saving/challenges',  // ✅ 진행 중 챌린지(다중) 상세 페이지
    name: 'ChallengeDetail',
    component: () => import('@/views/ChallengeDetail.vue')
  },
  {
    path: '/saving/challenges/select', // ✅ 챌린지 선택 페이지
    name: 'ChallengeSelect',
    component: () => import('@/views/ChallengeSelect.vue')
  },
  {
    path: '/saving/recommend', // 예적금 추천은 추후 구현
    name: 'SavingRecommend',
    component: Tab4ProductRecommend
  },

  // 주식
  { path: '/knowledge', component: StockKnowledge },
  { path: '/knowledge/:id', component: StockKnowledgeDetail, name: 'KnowledgeDetail' },
]


const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 인증이 필요한 페이지 보호
router.beforeEach((to, from, next) => {
  const isLoggedIn = !!localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: 'Login' })
  }
  next()
})

export default router
