<template>
  <div>
    <h3 class="text-2xl font-bold mb-6">📘 주식 기초 지식 카드</h3>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      <div
        v-for="(item, index) in knowledgeList"
        :key="index"
        class="rounded-lg overflow-hidden shadow hover:shadow-lg transition"
      >
        <div class="relative h-48 bg-gray-200">
          <img
            :src="item.image"
            alt="stock concept"
            class="w-full h-full object-cover"
          />
          <div class="absolute top-2 left-2 bg-black bg-opacity-60 text-white text-xs px-2 py-1 rounded">
            {{ index + 1 | twoDigits }}
          </div>
        </div>
        <div class="p-4">
          <h4 class="text-lg font-semibold mb-1">{{ item.title }}</h4>
          <p class="text-sm text-gray-600">{{ item.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StockKnowledge',
  data() {
    return {
      knowledgeList: [
        {
          title: 'PER이란?',
          description: '주가를 주당순이익으로 나눈 값으로, 낮을수록 저평가된 기업을 의미합니다.',
          image: 'https://via.placeholder.com/400x200?text=PER',
        },
        {
          title: 'PBR이란?',
          description: '주가를 주당순자산으로 나눈 지표로, 기업의 자산 대비 주가 수준을 보여줍니다.',
          image: 'https://via.placeholder.com/400x200?text=PBR',
        },
        {
          title: 'ROE란?',
          description: '자기자본이익률로, 기업이 자기자본을 얼마나 효율적으로 운영하는지를 나타냅니다.',
          image: 'https://via.placeholder.com/400x200?text=ROE',
        },
      ]
    }
  },
  filters: {
    twoDigits(val) {
      return val < 9 ? `0${val}` : val
    }
  }
}
</script>

<style scoped>
</style>
