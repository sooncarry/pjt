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

import Tab4ProductRecommend from '@/components/finance/Tab4ProductRecommend.vue'
import StockKnowledge from '@/components/stock/StockKnowledge.vue'
import StockKnowledgeDetail from '@/components/stock/StockKnowledgeDetail.vue'

import SamplePage from '@/views/SamplePage.vue' // 디자인 테스트

import FinanceGlossary from '@/components/education/FinanceGlossary.vue'
import ProductKnowledge from '@/components/education/ProductKnowledge.vue'
import NewsBoard from '@/components/education/NewsBoard.vue'
import QuizBoard from '@/components/education/QuizBoard.vue'

const routes = [
  // 기본
  { path: '/sample', name: 'SamplePage', component: SamplePage }, // 디자인 테스트

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
    component: Tab4ProductRecommend
  },

  // 주식
  { path: '/knowledge', component: StockKnowledge },
  { path: '/knowledge/:id', component: StockKnowledgeDetail, name: 'KnowledgeDetail' },

  // 교육
  { path: '/education/glossary', name: 'Glossary', component: FinanceGlossary },
  { path: '/education/products', name: 'ProductKnowledge', component: ProductKnowledge },
  { path: '/education/stocks', name: 'StockKnowledge', component: StockKnowledge },
  { path: '/education/news', name: 'NewsBoard', component: NewsBoard },
  { path: '/education/quiz', name: 'QuizBoard', component: QuizBoard },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // savedPosition이 있으면(뒤로가기/앞으로가기) 해당 위치로, 아니면 최상단으로 이동
    if (savedPosition) {
      return savedPosition
    } else {
      return { left: 0, top: 0 }
    }
  }
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
