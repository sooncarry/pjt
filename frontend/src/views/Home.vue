<template>
  <div>
    <section
      :class="[
        'hero-section text-white text-center shadow-sm position-relative overflow-hidden',
        { 'with-bg': !showIntro }
      ]"
>
      <!-- 인트로 애니메이션 -->
      <div
        v-if="showIntro"
        style="inset: 0"
        class="position-absolute d-flex justify-content-center align-items-center intro-container"
      >
        <img
          v-if="!showLogo"
          src="@/assets/money-12193.gif"
          class="intro-gif"
          alt="intro gif"
        />
        <img
          v-else
          src="@/assets/logo_tiggle_white.png"
          class="intro-logo animate__animated animate__fadeInDown"
          alt="tiggle logo"
        />
      </div>

      <!-- 인트로가 끝난 후 보여질 실제 콘텐츠 -->
      <div v-if="!showIntro" class="container">
        <h1 class="display-5 fw-bold mb-3">지금, 티끌로 금융 습관을 바꿔보세요</h1>
        <p class="lead">
          <strong>티끌 모아 태산!</strong><br />
          작은 습관 하나, 큰 변화의 시작이에요.<br />
          우리의 금융 습관, 이제 슬쩍 교정해볼까요?
        </p>
        <div class="mt-4 d-flex justify-content-center gap-3 flex-wrap">
          <RouterLink to="/saving" class="btn btn-light btn-lg rounded-pill px-4 fw-semibold">
            💰 저축 챌린지 시작하기
          </RouterLink>
          <RouterLink to="/finance" class="btn btn-outline-light btn-lg rounded-pill px-4 fw-semibold">
            🏦 예적금 추천받기
          </RouterLink>
        </div>
      </div>
    </section>



    <!-- 주요 서비스 안내 (이모지) -->
    <section class="container py-5">
      <div class="row text-center">
        <div class="col-md-4 mb-4">
          <div class="display-4 mb-2">📈</div>
          <h5 class="fw-bold">저축 챌린지</h5>
          <p class="text-muted">맞춤 챌린지로 꾸준한 저축 습관 만들기</p>
        </div>
        <div class="col-md-4 mb-4">
          <div class="display-4 mb-2">💳</div>
          <h5 class="fw-bold">예적금 금리 비교</h5>
          <p class="text-muted">내 월급 기준으로 가장 이득인 상품 추천</p>
        </div>
        <div class="col-md-4 mb-4">
          <div class="display-4 mb-2">💬</div>
          <h5 class="fw-bold">커뮤니티</h5>
          <p class="text-muted">같이 아끼고, 같이 부자되는 이야기</p>
        </div>
      </div>
    </section>

    <!-- 전체 너비 섹션 (카드 5개 각각 한 줄씩) -->
    <section class="py-0">
    <!-- 금융 -->
      <div class="feature-row" :style="{ background: '#E6DEFF' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h3 class="fw-bold text-dark py-2">금융상품 비교</h3>
            <p class="text-dark mb-0">예금, 적금, 대출까지<br />나에게 딱 맞는 상품을 추천해드려요.</p>
          </div>
          <RouterLink to="/finance" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 주식 -->
      <div class="feature-row" :style="{ background: '#D9D5FF' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h3 class="fw-bold text-dark py-2">주식 정보 탐색</h3>
            <p class="text-dark mb-0">차근차근 배우고<br />종목도 쉽게 비교할 수 있어요.</p>
          </div>
          <RouterLink to="/stock" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 교육 -->
      <div class="feature-row" :style="{ background: '#F1F3F5' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h3 class="fw-bold py-2">금융 교육 콘텐츠</h3>
            <p class="mb-0">기초 개념부터 퀴즈까지<br />재미있게 배우는 금융 지식!</p>
          </div>
          <RouterLink to="/education" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 저축 -->
      <div class="feature-row" :style="{ background: '#5a45ff' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5 text-white" >
          <div>
            <h3 class="fw-bold py-2">저축 챌린지</h3>
            <p class="mb-0">목표형 저축 습관을 만들고<br />달성해보세요.</p>
          </div>
          <RouterLink to="/saving" class="btn btn-outline-light rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 커뮤니티 -->
      <div class="feature-row" :style="{ background: '#F1F3F5' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h3 class="fw-bold text-dark py-2">커뮤니티</h3>
            <p class="text-dark mb-0">재테크 이야기부터 꿀팁까지<br />함께 나누고 성장해요.</p>
          </div>
          <RouterLink to="/community" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const showIntro = ref(true)
const showLogo = ref(false)

onMounted(() => {
  // 4.5초 후 gif 사라지고 로고 등장
  setTimeout(() => {
    showLogo.value = true
  }, 4500)

  // 로고는 1.2초 보여주고 전체 인트로 종료
  setTimeout(() => {
    showIntro.value = false
  }, 5700)
})

</script>

<style scoped>
/* 애니메이션용 */
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';

h1, h5 {
  font-family: 'Cafe24Simplehae', 'Noto Sans KR', sans-serif;
}
.hero-section {
  background-color: #5A45FF;
  min-height: 520px;
  padding: 120px 0;
  position: relative;
  overflow: hidden;
}

/* 배경 이미지는 인트로 종료 후에만 적용 */
.hero-section.with-bg {
  background-image: url('@/assets/your_bg_image.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 모바일 배경 이미지도 조건부 클래스에만 적용 */
@media (max-width: 768px) {
  .hero-section.with-bg {
    background-image: url('@/assets/your_bg_image_mobile.png');
  }
}


/* 인트로는 section 영역 내부에서만 절대 위치 */
.intro-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #5A45FF;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

/* 이미지 스타일 */
.intro-gif {
  height: 700px;
  width: auto;
}

.intro-logo {
  width: 240px;
  height: auto;
}
</style>