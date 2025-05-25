<template>
  <div class="container my-4" @click.self="hideSuggestions">
    <h2 class="h5 fw-semibold mb-4">📢 공시 정보 검색</h2>

    <!-- 검색창 + 자동완성 + 버튼 -->
    <div class="row g-3 align-items-start mb-4 position-relative">
      <!-- 입력 -->
      <div class="col-md-4 position-relative">
        <input
          v-model="companyName"
          @input="fetchSuggestions"
          @focus="showSuggestions = true"
          type="text"
          placeholder="기업명을 입력하세요"
          class="form-control form-control-sm rounded-3"
        />
        <!-- 자동완성 드롭다운 -->
        <ul
          v-if="suggestions.length && showSuggestions"
          class="list-group position-absolute w-100 mt-1 shadow z-3"
          style="max-height: 200px; overflow-y: auto;"
        >
          <li
            v-for="(s, index) in suggestions"
            :key="index"
            @click="selectSuggestion(s.name)"
            class="list-group-item list-group-item-action small"
            style="cursor: pointer;"
          >
            {{ s.name }}
          </li>
        </ul>
      </div>

      <!-- 검색 버튼 -->
      <div class="col-md-auto">
        <button @click="fetchDisclosures(true)" class="btn btn-success btn-sm rounded-pill px-4">
          🔍 검색
        </button>
      </div>

      <!-- 기간 선택 버튼 -->
      <div class="col-md">
        <div class="d-flex flex-wrap gap-2">
          <button
            v-for="(label, value) in periods"
            :key="value"
            @click="setPeriod(value)"
            class="btn btn-sm rounded-pill"
            :class="selectedPeriod === value ? 'btn-primary text-white' : 'btn-outline-primary'"
          >
            {{ label }}
          </button>
        </div>
      </div>
    </div>

    <!-- 로딩 -->
    <div v-if="loading" class="text-muted mb-4 small">⏳ 공시 정보를 불러오는 중...</div>

    <!-- 공시 카드 리스트 -->
    <div v-else-if="disclosures.length" class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4">
      <div v-for="(item, index) in pagedDisclosures" :key="index" class="col">
        <div class="card h-100 shadow-sm border-0 rounded-4">
          <div class="card-body">
            <h5 class="card-title text-primary fw-semibold mb-2">{{ item.title }}</h5>
            <p class="card-subtitle mb-1 text-muted small">📅 {{ formatDate(item.date) }}</p>
            <p class="card-subtitle mb-2 text-muted small">🏢 {{ item.corp_name }}</p>
            <a
              :href="item.link"
              target="_blank"
              class="btn btn-sm btn-outline-primary rounded-pill mt-2"
            >
              공시 보기 →
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div v-if="!loading && totalPages > 1" class="mt-5 d-flex justify-content-center flex-wrap gap-2">
      <button
        v-if="pageGroup > 1"
        @click="prevPageGroup"
        class="btn btn-sm btn-outline-secondary rounded-pill"
      >
        ◀ 이전
      </button>

      <button
        v-for="n in visiblePages"
        :key="n"
        @click="page = n"
        class="btn btn-sm rounded-pill"
        :class="page === n ? 'btn-primary text-white fw-bold' : 'btn-outline-primary'"
      >
        {{ n }}
      </button>

      <button
        v-if="pageGroup * pageGroupSize < totalPages"
        @click="nextPageGroup"
        class="btn btn-sm btn-outline-secondary rounded-pill"
      >
        다음 ▶
      </button>
    </div>

    <!-- 데이터 없음 -->
    <div v-else-if="!loading && !disclosures.length" class="text-muted mt-4">📭 공시가 없습니다.</div>
  </div>
</template>

<script>
export default {
  name: "StockInterestInfo",
  data() {
    return {
      companyName: "",
      selectedPeriod: 30,
      periods: {
        30: "1개월",
        90: "3개월",
        180: "6개월",
        365: "12개월",
        all: "전체보기",
      },
      disclosures: [],
      loading: false,
      page: 1,
      pageSize: 15,
      pageGroup: 1,
      pageGroupSize: 5,
      suggestions: [],
      showSuggestions: false,
      debounceTimeout: null,
    };
  },
  computed: {
    pagedDisclosures() {
      const start = (this.page - 1) * this.pageSize;
      return this.disclosures.slice(start, start + this.pageSize);
    },
    totalPages() {
      return Math.ceil(this.disclosures.length / this.pageSize);
    },
    visiblePages() {
      const start = (this.pageGroup - 1) * this.pageGroupSize + 1;
      const end = Math.min(start + this.pageGroupSize - 1, this.totalPages);
      const pages = [];
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    },
  },
  methods: {
    hideSuggestions() {
      this.showSuggestions = false;
    },
    setPeriod(days) {
      this.selectedPeriod = days;
      this.page = 1;
      this.pageGroup = 1;
      this.fetchDisclosures(true);
    },
    fetchSuggestions() {
      if (this.debounceTimeout) clearTimeout(this.debounceTimeout);

      this.debounceTimeout = setTimeout(() => {
        if (this.companyName.trim().length < 1) {
          this.suggestions = [];
          this.showSuggestions = false;
          return;
        }

        fetch(`/api/stock/search/?query=${encodeURIComponent(this.companyName.trim())}`)
          .then((res) => res.json())
          .then((data) => {
            this.suggestions = data;
            this.showSuggestions = true;
          });
      }, 200);
    },
    selectSuggestion(name) {
      this.companyName = name;
      this.showSuggestions = false;
      this.page = 1;
      this.pageGroup = 1;
      this.fetchDisclosures(true);
    },
    fetchDisclosures(reset = false) {
      this.loading = true;
      if (reset) {
        this.page = 1;
        this.pageGroup = 1;
      }

      const today = new Date();
      let bgnDate = "20000101";
      if (this.selectedPeriod !== "all") {
        const start = new Date(today);
        start.setDate(today.getDate() - this.selectedPeriod);
        bgnDate = start.toISOString().slice(0, 10).replace(/-/g, "");
      }

      const query = this.companyName.trim();
      const url = query
        ? `/api/stock/disclosures/?query=${encodeURIComponent(query)}&bgn_de=${bgnDate}&page_group=1`
        : `/api/stock/disclosures/?bgn_de=${bgnDate}&page_group=1`;

      fetch(url)
        .then((res) => res.json())
        .then((data) => {
          this.disclosures = data.disclosures || [];
          this.loading = false;
        })
        .catch((err) => {
          console.error("공시 로딩 실패:", err);
          this.loading = false;
        });
    },
    nextPageGroup() {
      this.pageGroup++;
      this.page = (this.pageGroup - 1) * this.pageGroupSize + 1;
      this.fetchDisclosures();
    },
    prevPageGroup() {
      if (this.pageGroup > 1) {
        this.pageGroup--;
        this.page = (this.pageGroup - 1) * this.pageGroupSize + 1;
        this.fetchDisclosures();
      }
    },
    formatDate(dateStr) {
      return `${dateStr.slice(0, 4)}-${dateStr.slice(4, 6)}-${dateStr.slice(6)}`;
    },
  },
  mounted() {
    this.fetchDisclosures();
  },
};
</script>

<style scoped>
input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}
</style>
