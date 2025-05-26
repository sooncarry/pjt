<template>
  <div>
    <!-- 메인 헤더 영역 -->
    <section class="text-white text-center py-5 shadow-sm" :style="{ background: `url(${bgImage}) no-repeat center / cover` }">
      <div class="container">
        <h1 class="display-5 fw-bold mb-3">지금, 금융 습관을 바꾸세요</h1>
        <p class="lead">차근차근 모으는 힘, 우리 함께해요</p>
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
            <h4 class="fw-bold text-dark">금융상품 비교</h4>
            <p class="text-dark mb-0">예금, 적금, 대출까지<br />나에게 딱 맞는 상품을 추천해드려요.</p>
          </div>
          <RouterLink to="/finance" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 주식 -->
      <div class="feature-row" :style="{ background: '#D9D5FF' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h4 class="fw-bold text-dark">주식 정보 탐색</h4>
            <p class="text-dark mb-0">차근차근 배우고<br />종목도 쉽게 비교할 수 있어요.</p>
          </div>
          <RouterLink to="/stock" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 교육 -->
      <div class="feature-row" :style="{ background: '#F1F3F5' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h4 class="fw-bold">금융 교육 콘텐츠</h4>
            <p class="mb-0">기초 개념부터 퀴즈까지<br />재미있게 배우는 금융 지식!</p>
          </div>
          <RouterLink to="/education" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 저축 -->
      <div class="feature-row" :style="{ background: '#5a45ff' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5 text-white" >
          <div>
            <h4 class="fw-bold">저축 챌린지</h4>
            <p class="mb-0">목표형 저축 습관을 만들고<br />달성해보세요.</p>
          </div>
          <RouterLink to="/saving" class="btn btn-outline-light rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>

      <!-- 커뮤니티 -->
      <div class="feature-row" :style="{ background: '#F1F3F5' }">
        <div class="container d-flex justify-content-between align-items-center flex-wrap py-5">
          <div>
            <h4 class="fw-bold text-dark">커뮤니티</h4>
            <p class="text-dark mb-0">재테크 이야기부터 꿀팁까지<br />함께 나누고 성장해요.</p>
          </div>
          <RouterLink to="/community" class="btn btn-outline-dark rounded-pill px-4">바로가기</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import bgImage from '@/assets/your_bg_image.png'
import bg1 from '@/assets/lightpurple1.png'
import bg2 from '@/assets/lightpurple2.png'
import bg3 from '@/assets/green.png'
import bg4 from '@/assets/lightgreen.png'
</script>

<style scoped>
h1, h5 {
  font-family: 'Cafe24Simplehae', 'Noto Sans KR', sans-serif;
}
</style>
