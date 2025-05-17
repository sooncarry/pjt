import { createRouter, createWebHistory } from 'vue-router'

// 기본 페이지
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import MyPage from '../views/MyPage.vue'

// 기타 기능 페이지
import Community from '../views/Community.vue'
import NearbyBank from '../views/NearbyBank.vue'
import Interest from '../views/Interest.vue'
import Recommend from '../views/Recommend.vue'
import Savings from '../views/Savings.vue'
import Commodity from '../views/Commodity.vue'
import Deposit from '../views/Deposit.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/mypage', name: 'MyPage', component: MyPage, meta: { requiresAuth: true } },

  // 한글 메뉴에 대응하는 영문 path
  { path: '/interest', name: 'Interest', component: Deposit },         // 예적금 금리 비교
  { path: '/commodity', name: 'Commodity', component: Commodity },     // 현물 상품 비교
  { path: '/recommend', name: 'Recommend', component: Recommend },     // 금융 상품 추천
  { path: '/savings', name: 'Savings', component: Savings },           // 저축
  { path: '/deposit', name: 'Deposit', component: Interest },          // 예금
  { path: '/nearby-bank', name: 'NearbyBank', component: NearbyBank },// 근처 은행 검색
  { path: '/community', name: 'Community', component: Community },     // 커뮤니티
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

export default router;