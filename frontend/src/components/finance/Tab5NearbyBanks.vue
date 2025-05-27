<template>
  <div class="container my-4">
    <h2 class="fw-semibold mb-4">📍 근처 은행 찾기</h2>

    <!-- 검색 폼 -->
    <div class="row gy-2 align-items-end mb-3">
      <div class="col-md-3">
        <label class="form-label small">광역시/도</label>
        <select class="form-select form-select-sm" v-model="selectedSido" @change="updateSigungu">
          <option value="">선택</option>
          <option v-for="sido in sidoList" :key="sido">{{ sido }}</option>
        </select>
      </div>

      <div class="col-md-3">
        <label class="form-label small">시/군/구</label>
        <select class="form-select form-select-sm" v-model="selectedSigungu" :disabled="!selectedSido">
          <option value="">선택</option>
          <option v-for="sigungu in sigunguList" :key="sigungu">{{ sigungu }}</option>
        </select>
      </div>

      <div class="col-md-3">
        <label class="form-label small">은행</label>
        <select class="form-select form-select-sm" v-model="selectedBank" :disabled="filterType === 'ATM'">
          <option value="">(전체)</option>
          <option v-for="bank in bankList" :key="bank">{{ bank }}</option>
        </select>
      </div>

      <div class="col-md-3">
        <button @click="searchBanks" class="btn btn-primary btn-sm rounded-pill w-100">
          🔍 찾기
        </button>
      </div>
    </div>

    <!-- 은행 / ATM 토글 -->
    <div class="btn-group mb-3" role="group">
      <button
        type="button"
        class="btn btn-outline-secondary btn-sm"
        :class="{ active: filterType === 'BANK' }"
        @click="setFilter('BANK')"
      >
        은행
      </button>
      <button
        type="button"
        class="btn btn-outline-secondary btn-sm"
        :class="{ active: filterType === 'ATM' }"
        @click="setFilter('ATM')"
      >
        ATM
      </button>
    </div>

    <!-- 지도 + 결과 리스트 -->
    <div class="row g-3">
      <!-- 결과 리스트 -->
      <div class="col-lg-4 order-lg-0 order-1">
        <ul class="list-group overflow-auto" style="max-height: 600px" ref="resultList">
          <li
            v-for="(place, idx) in places"
            :key="place.id || idx"
            class="list-group-item list-group-item-action d-flex justify-content-between align-items-start"
            :class="{ active: selectedIdx === idx }"
            @click="focusPlace(idx)"
          >
            <div>
              <div class="fw-semibold">{{ place.place_name }}</div>
              <small class="text-muted">{{ place.road_address_name || place.address_name }}</small>
            </div>
            <span class="badge bg-primary rounded-pill">{{ place.distanceKm }} km</span>
          </li>
        </ul>
      </div>

      <!-- 지도 -->
      <div class="col-lg-8 order-lg-1 order-0">
        <div id="map" style="width: 100%; height: 600px;" class="rounded-3 border"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { loadKakaoMapScript } from '@/utils/loadKakaoMapScript'

// ----------- 상태 ----------- //
const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')
const filterType = ref('BANK')            // BANK | ATM

const sidoList = ref([])
const sigunguList = ref([])
const bankList = ref([])

const map = ref(null)
const userLatLng = ref(null)
const markers = ref([])
const infoWindows = ref([])
const places = ref([])
const selectedIdx = ref(null)

const rawData = ref(null)
const resultList = ref(null)

// ----------- 헬퍼 ----------- //
function haversine(lat1, lon1, lat2, lon2) {
  const toRad = deg => (deg * Math.PI) / 180
  const R = 6371
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

function setFilter(type) {
  if (filterType.value === type) return
  filterType.value = type
  searchBanks()
}

function clearMarkers() {
  markers.value.forEach(m => m.setMap(null))
  markers.value = []
  infoWindows.value = []
}

function closeAllInfo() {
  infoWindows.value.forEach(iw => iw.close())
}

function filterByType(resultArray) {
  return resultArray.filter(p => {
    const cat = p.category_name || ''
    if (filterType.value === 'BANK') {
      return /은행/i.test(cat) && !/ATM/i.test(cat)
    }
    // ATM 모드
    return /ATM|현금자동/i.test(cat)
  })
}

function buildListAndMarkers(searchResults) {
  const filtered = filterByType(searchResults)
  if (!filtered.length) {
    clearMarkers()
    places.value = []
    return alert('표시할 결과가 없습니다.')
  }

  const enriched = filtered.map(p => {
    const dist = haversine(userLatLng.value.getLat(), userLatLng.value.getLng(), +p.y, +p.x)
    return { ...p, distanceKm: dist.toFixed(2) }
  })
  enriched.sort((a, b) => a.distanceKm - b.distanceKm)
  places.value = enriched

  const bounds = new window.kakao.maps.LatLngBounds()
  clearMarkers()

  enriched.forEach((place, idx) => {
    const position = new window.kakao.maps.LatLng(place.y, place.x)
    const marker = new window.kakao.maps.Marker({ map: map.value, position })
    const iw = new window.kakao.maps.InfoWindow({ content: `<div style="padding:5px;font-size:13px;">${place.place_name}</div>` })

    window.kakao.maps.event.addListener(marker, 'click', () => selectPlace(idx))

    markers.value.push(marker)
    infoWindows.value.push(iw)
    bounds.extend(position)
  })

  map.value.setBounds(bounds)
}

function selectPlace(idx) {
  selectedIdx.value = idx
  closeAllInfo()
  const marker = markers.value[idx]
  const iw = infoWindows.value[idx]
  iw.open(map.value, marker)
  map.value.panTo(marker.getPosition())
  if (resultList.value) {
    resultList.value.children[idx]?.scrollIntoView({ block: 'nearest' })
  }
}

function focusPlace(idx) {
  selectPlace(idx)
}

// ----------- 초기화 ----------- //
async function init() {
  const res = await import('@/assets/data.json')
  rawData.value = res.default
  sidoList.value = rawData.value.mapInfo.map(item => item.name)
  bankList.value = rawData.value.bankInfo

  await loadKakaoMapScript()
  initMap()
  locateUserAndSearchNearby()
}

function initMap() {
  const center = new window.kakao.maps.LatLng(37.49818, 127.027386)
  map.value = new window.kakao.maps.Map(document.getElementById('map'), { center, level: 3 })
}

function locateUserAndSearchNearby() {
  if (!navigator.geolocation) return alert('브라우저에서 위치 정보를 지원하지 않습니다.')

  navigator.geolocation.getCurrentPosition(
    pos => {
      const { latitude: lat, longitude: lng } = pos.coords
      userLatLng.value = new window.kakao.maps.LatLng(lat, lng)
      map.value.setCenter(userLatLng.value)

      new window.kakao.maps.Marker({
        position: userLatLng.value,
        map: map.value,
        image: new window.kakao.maps.MarkerImage(
          'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
          new window.kakao.maps.Size(40, 42),
          { offset: new window.kakao.maps.Point(13, 42) }
        )
      })

      // 행정구역 자동 선택
      const geocoder = new window.kakao.maps.services.Geocoder()
      geocoder.coord2RegionCode(lng, lat, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK && result.length) {
          const region = result.find(r => r.region_type === 'H') || result[0]
          selectedSido.value = region.region_1depth_name
          updateSigungu()
          selectedSigungu.value = region.region_2depth_name
        }
      })

      // 기본 검색
      const ps = new window.kakao.maps.services.Places()
      ps.keywordSearch(filterType.value === 'ATM' ? 'ATM' : '은행', (results, status) => {
        if (status === window.kakao.maps.services.Status.OK) buildListAndMarkers(results)
      }, { location: userLatLng.value, radius: 5000 })
    },
    err => console.warn('❗ 위치 정보 접근 실패:', err.message),
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  )
}

// ----------- 드롭다운 & 검색 ----------- //
function updateSigungu() {
  selectedSigungu.value = ''
  const selected = rawData.value.mapInfo.find(item => item.name === selectedSido.value)
  sigunguList.value = selected ? selected.countries : []
}

function searchBanks() {
  if (!selectedSido.value || !selectedSigungu.value) {
    return alert('광역시/도와 시/군/구를 선택하세요.')
  }

  const ps = new window.kakao.maps.services.Places()
  let keyword = ''
  if (filterType.value === 'ATM') {
    keyword = 'ATM'
  } else {
    keyword = selectedBank.value ? `${selectedBank.value} 은행` : '은행'
  }
  const query = `${selectedSido.value} ${selectedSigungu.value} ${keyword}`

  ps.keywordSearch(query, (results, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      buildListAndMarkers(results)
    } else {
      clearMarkers()
      places.value = []
      alert('검색 결과가 없습니다.')
    }
  })
}

// ----------- 지도 이벤트 : 인포윈도우 닫기 ----------- //
watch(map, newVal => {
  if (newVal) {
    window.kakao.maps.event.addListener(newVal, 'dragstart', closeAllInfo)
    window.kakao.maps.event.addListener(newVal, 'zoom_start', closeAllInfo)
  }
})

onMounted(init)
</script>

<style scoped>
.list-group-item.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: #fff;
}
</style>