<template>
  <div class="intro-wrapper">
    <!-- 떨어지는 문구 -->
    <div class="stack-group">
      <div
        v-for="(line, index) in lines"
        :key="line"
        class="stack-line"
        :style="{
          top: `${(2 - index) * 60}px`,
          animationDelay: `${index * 0.7}s`
        }"
      >
        {{ line }}
      </div>
    </div>

    <!-- MoneyStack 중앙 등장 -->
    <div v-if="showTitle" class="moneystack-logo-wrapper">
      <h1 class="moneystack-logo">MoneyStack</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Intro',
  data() {
    return {
      fullLines: ['기록을 쌓다', '습관을 쌓다', '돈을 쌓는다'],
      lines: [],
      showTitle: false
    };
  },
  mounted() {
  this.runIntro();
},
methods: {
  runIntro() {
    let i = 0;
    const interval = setInterval(() => {
      this.lines.push(this.fullLines[i]);
      i++;
      if (i === this.fullLines.length) {
        clearInterval(interval);

        // 문장 사라짐
        setTimeout(() => {
          this.lines = [];
        }, 2000);

        // MoneyStack 등장
        setTimeout(() => {
          this.showTitle = true;
        }, 2700);

        // ❗ 마지막에 emit: 반드시 충분히 보여진 뒤
        setTimeout(() => {
          this.$emit('finished');
        }, 4000);
      }
    }, 700);
  }
}}

</script>

<style scoped>
.intro-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: #5A45FF; /* primary */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  font-family: 'Pretendard', sans-serif;
}

.stack-group {
  position: relative;
  width: 100%;
  height: 200px;
}

.stack-line {
  position: absolute;
  width: 100%;
  text-align: center;
  font-size: 2rem;
  font-weight: 600;
  color: white;
  opacity: 0;
  animation: drop 0.6s ease-out forwards;
}

@keyframes drop {
  0% {
    opacity: 0;
    transform: translateY(-100px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.moneystack-logo-wrapper {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 999;
}

.moneystack-logo {
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  letter-spacing: 0.2em;
  opacity: 0;
  animation: fadeInScale 1s ease-out forwards;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
