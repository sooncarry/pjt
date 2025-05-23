import { createRouter, createWebHistory } from 'vue-router'

// 기본 페이지
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import MyPage from '../views/MyPage.vue'
import ChecklistPage from '@/views/ChecklistPage.vue'

// 주요 기능 페이지
import Finance from '../views/Finance.vue'
import Stock from '../views/Stock.vue'
import Education from '../views/Education.vue'
import Saving from '../views/Saving.vue'
import Community from '../views/Community.vue'

// 커뮤니티 게시판 페이지
import PostDetail from '../views/PostDetail.vue'
import PostForm from '../views/PostForm.vue'

const routes = [
  // 기본
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/mypage', name: 'MyPage', component: MyPage, meta: { requiresAuth: true } },
  { path: '/checklist', name: 'Checklist', component: ChecklistPage },

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
    component: { template: '<div style="padding: 2rem;">(예적금 추천은 준비 중입니다.)</div>' }
  }
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
