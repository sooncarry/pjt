import { createRouter, createWebHistory } from 'vue-router'

// 기본 페이지
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import MyPage from '../views/MyPage.vue'

// 주요 기능 페이지
import Finance from '../views/Finance.vue'
import Stock from '../views/Stock.vue'
import Education from '../views/Education.vue'
import Saving from '../views/Saving.vue'
import Community from '../views/Community.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/mypage', name: 'MyPage', component: MyPage, meta: { requiresAuth: true } },

  // 주요 뷰 경로
  { path: '/finance', name: 'Finance', component: Finance },
  { path: '/stock', name: 'Stock', component: Stock },
  { path: '/education', name: 'Education', component: Education },
  { path: '/saving', name: 'Saving', component: Saving },
  { path: '/community', name: 'Community', component: Community },
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
