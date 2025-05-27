<template>
  <section class="py-5 bg-light position-relative">
    <div class="container position-relative">
        <div class="swiper-button-prev custom-nav-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5A45FF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6" />
            </svg>
        </div>
        <div class="swiper-button-next custom-nav-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#5A45FF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6" />
            </svg>
        </div>

        <swiper
        :modules="[Navigation]"
        :navigation="swiperNavigation"
        :slides-per-view="1"
        :space-between="20"
        :loop="true"
        class="custom-swiper"
        >
        <swiper-slide v-for="(feature, index) in features" :key="index">
          <div class="d-flex flex-column flex-lg-row align-items-center justify-content-between p-4 rounded-4 bg-white shadow-sm">
            <!-- 왼쪽 이미지 -->
            <img :src="feature.image" alt="feature image" class="slide-image mb-4 mb-lg-0 me-lg-5" />

            <!-- 오른쪽 텍스트 -->
            <div class="text-lg-start text-center">
              <p class="text-primary fw-semibold mb-2">{{ feature.subtitle }}</p>
              <h2 class="fw-bold mb-3">{{ feature.title }}</h2>
              <p class="text-muted mb-4">{{ feature.desc }}</p>
              <RouterLink :to="feature.to" class="cta-button">{{ feature.buttonText }}</RouterLink>
            </div>
          </div>
        </swiper-slide>
        </swiper>
    </div> 
  </section>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/navigation'
import 'bootstrap-icons/font/bootstrap-icons.css' // 아이콘 사용 시

const swiperNavigation = {
  nextEl: '.swiper-button-next',
  prevEl: '.swiper-button-prev',
}

const features = [
  {
    title: '금융상품 비교',
    subtitle: '금융상품',
    desc: '예금, 적금, 대출까지\n나에게 꼭 맞는 금융 상품을 비교하고 추천받을 수 있어요.',
    buttonText: '상품 비교하러 가기 →',
    to: '/finance',
    image: new URL('@/assets/logo_tiggle.png',import.meta.url).href,
  },
  {
    title: '주식 정보 탐색',
    subtitle: '주식',
    desc: '기초 개념부터 종목 비교까지\n주식의 모든 정보를 쉽게 탐색할 수 있어요.',
    buttonText: '주식 정보 보러 가기 →',
    to: '/stock',
    image: new URL('@/assets/logo_tiggle.png',import.meta.url).href,
  },
  {
    title: '금융 교육 콘텐츠',
    subtitle: '금융 교육',
    desc: '퀴즈부터 개념 설명까지\n지루하지 않게 배우는 금융 지식!',
    buttonText: '지금 배우러 가기 →',
    to: '/education',
    image: new URL('@/assets/logo_tiggle.png',import.meta.url).href,
  },
  {
    title: '저축 챌린지',
    subtitle: '저축',
    desc: '목표 금액과 기간 설정하고\n꾸준한 저축 습관을 만들어보세요.',
    buttonText: '챌린지 시작하기 →',
    to: '/saving',
    image: new URL('@/assets/logo_tiggle.png',import.meta.url).href,
  },
  {
    title: '커뮤니티',
    subtitle: '커뮤니티',
    desc: '재테크 이야기부터 꿀팁까지\n함께 나누고 성장해요.',
    buttonText: '바로가기 →',
    to: '/community',
    image: new URL('@/assets/logo_tiggle.png',import.meta.url).href,
  },
]
</script>

<style scoped>

.custom-swiper {
  padding: 1rem 0;
}

.slide-image {
  width: 240px;
  max-width: 100%;
}

.cta-button {
  padding: 12px 20px;
  border: 1px solid #111;
  border-radius: 999px;
  color: #111;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  display: inline-block;
}

.cta-button:hover {
  background-color: #111;
  color: white;
}

.custom-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: transparent;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 10;
  transition: background-color 0.2s ease;
}

.custom-nav-btn:hover {
  background-color: rgba(90, 69, 255, 0.08);
  border-radius: 50%;
}

.swiper-button-prev::after,
.swiper-button-next::after {
  display: none !important;
}

.swiper-button-prev {
  left: -5px;
}

.swiper-button-next {
  right: -5px;
}
</style>
