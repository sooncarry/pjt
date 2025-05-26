<template>
  <div class="container my-4">
    <h2 class="fw-semibold mb-4">📍 근처 은행 찾기</h2>

    <div class="row gy-2 align-items-end mb-4">
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
        <select class="form-select form-select-sm" v-model="selectedBank">
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

    <div id="map" style="width: 100%; height: 600px;" class="rounded-3 border"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { loadKakaoMapScript } from '@/utils/loadKakaoMapScript'

const selectedSido = ref('')
const selectedSigungu = ref('')
const selectedBank = ref('')

const sidoList = ref([])
const sigunguList = ref([])
const bankList = ref([])

const map = ref(null)
const markers = ref([])
const rawData = ref(null)

onMounted(async () => {
  const res = await import('@/assets/data.json')
  rawData.value = res.default
  sidoList.value = rawData.value.mapInfo.map(item => item.name)
  bankList.value = rawData.value.bankInfo

  await loadKakaoMapScript()
  initMap()

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
      const lat = pos.coords.latitude
      const lng = pos.coords.longitude
      const userLocation = new window.kakao.maps.LatLng(lat, lng)

      map.value.setCenter(userLocation)

      const userMarker = new window.kakao.maps.Marker({
        position: userLocation,
        map: map.value,
        image: new window.kakao.maps.MarkerImage(
          'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
          new window.kakao.maps.Size(40, 42),
          { offset: new window.kakao.maps.Point(13, 42) }
        )
      })

      const geocoder = new window.kakao.maps.services.Geocoder()
      geocoder.coord2RegionCode(lng, lat, (result, status) => {
        if (status === window.kakao.maps.services.Status.OK && result.length > 0) {
          const regionH = result.find(r => r.region_type === 'H') || result[0]

          const fullAddress = `${regionH.region_1depth_name} ${regionH.region_2depth_name} ${regionH.region_3depth_name}`

          const infowindow = new window.kakao.maps.InfoWindow({
            content: `<div style="padding:5px;font-size:14px;">내 위치<br/>(${fullAddress})</div>`
          })
          infowindow.open(map.value, userMarker)

          // 드롭다운 자동 설정
          selectedSido.value = regionH.region_1depth_name
          updateSigungu()
          selectedSigungu.value = regionH.region_2depth_name
        }
      })

      const ps = new window.kakao.maps.services.Places()
      ps.keywordSearch('은행', (results, status) => {
        if (status === window.kakao.maps.services.Status.OK) {
          const bounds = new window.kakao.maps.LatLngBounds()
          bounds.extend(userLocation)

          results.forEach(place => {
            const position = new window.kakao.maps.LatLng(place.y, place.x)
            const marker = new window.kakao.maps.Marker({ map: map.value, position })

            const infowindow = new window.kakao.maps.InfoWindow({
              content: `<div style="padding:5px;font-size:14px;">${place.place_name}</div>`
            })

            window.kakao.maps.event.addListener(marker, 'click', () => {
              infowindow.open(map.value, marker)
            })

            markers.value.push(marker)
            bounds.extend(position)
          })

          map.value.setBounds(bounds)
        }
      }, { location: userLocation, radius: 5000 })
    }, err => {
      console.warn('❗ 위치 정보 접근 실패:', err.message)
    }, {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    })
  }
})

function updateSigungu() {
  selectedSigungu.value = ''
  const selected = rawData.value.mapInfo.find(item => item.name === selectedSido.value)
  sigunguList.value = selected ? selected.countries : []
}

function initMap() {
  const center = new window.kakao.maps.LatLng(37.49818, 127.027386)
  map.value = new window.kakao.maps.Map(document.getElementById('map'), {
    center,
    level: 4
  })
}

function searchBanks() {
  if (!selectedSido.value || !selectedSigungu.value) {
    alert('광역시/도와 시군구는 반드시 선택해야 합니다.')
    return
  }

  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []

  const ps = new window.kakao.maps.services.Places()
  const query = selectedBank.value
    ? `${selectedSido.value} ${selectedSigungu.value} ${selectedBank.value}`
    : `${selectedSido.value} ${selectedSigungu.value} 은행`

  ps.keywordSearch(query, (results, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const bounds = new window.kakao.maps.LatLngBounds()

      results.forEach(place => {
        const position = new window.kakao.maps.LatLng(place.y, place.x)
        const marker = new window.kakao.maps.Marker({ map: map.value, position })

        const infowindow = new window.kakao.maps.InfoWindow({
          content: `<div style="padding:5px;font-size:14px;">${place.place_name}</div>`
        })

        window.kakao.maps.event.addListener(marker, 'click', () => {
          infowindow.open(map.value, marker)
        })

        markers.value.push(marker)
        bounds.extend(position)
      })

      map.value.setBounds(bounds)
    } else {
      alert('검색 결과가 없습니다.')
    }
  })
}
</script>

<style scoped>
/* 이전 select 스타일은 Bootstrap form-select로 대체되어 제거 가능 */
</style>
