<template>
  <div>
    <div id="blackContainer"></div>
    <p id="title">🍿{{ userInfo.nickname }}님 근처 영화관</p>
    <div class="map_wrap">
      <div id="map"></div>
      <div id="menu_wrap" class="bg_white">
        <div class="option">
          <div>
            <form @submit.prevent="searchPlaces">
              키워드 : <input type="text" v-model="keyword" size="15" />
              <button type="submit">검색하기</button>
            </form>
          </div>
        </div>
        <hr />
        <ul id="placesList"></ul>
        <div id="pagination"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const store = useAuthStore();
const userInfo = ref(store.userdetail);
const keyword = ref(`${userInfo.value.location} 근처 영화관`);
const markers = ref([]);
let map;
let infowindow;
let ps;

const initMap = () => {
  const mapContainer = document.getElementById('map');
  const mapOption = {
    center: new kakao.maps.LatLng(userInfo.value.latitude_y, userInfo.value.longitude_x),
    level: 2,
  };

  map = new kakao.maps.Map(mapContainer, mapOption);
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
  ps = new kakao.maps.services.Places();

  // 현재 위치를 표시하는 마커를 생성하고 지도에 추가
  const markerPosition = 
     new kakao.maps.LatLng(userInfo.value.latitude_y, userInfo.value.longitude_x)
    ;
  const marker = new kakao.maps.Marker({
    position: markerPosition
  });
  marker.setMap(map);

  searchPlaces();

};

const searchPlaces = () => {
  const keywordValue = keyword.value.trim();
  if (!keywordValue) {
    alert('키워드를 입력해주세요!');
    return;
  }
  ps.keywordSearch(keywordValue, placesSearchCB);
};

const placesSearchCB = (data, status, pagination) => {
  if (status === kakao.maps.services.Status.OK) {
    displayPlaces(data);
    displayPagination(pagination);
  } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
    alert('검색 결과가 존재하지 않습니다.');
  } else if (status === kakao.maps.services.Status.ERROR) {
    alert('검색 결과 중 오류가 발생했습니다.');
  }
};

const displayPlaces = (places) => {
  const listEl = document.getElementById('placesList');
  const menuEl = document.getElementById('menu_wrap');
  const fragment = document.createDocumentFragment();
  const bounds = new kakao.maps.LatLngBounds();

  removeAllChildNods(listEl);
  removeMarker();

  for (let i = 0; i < places.length; i++) {
    const placePosition = new kakao.maps.LatLng(places[i].y, places[i].x);
    const marker = addMarker(placePosition, i);
    const itemEl = getListItem(i, places[i]);

    bounds.extend(placePosition);

    (function (marker, title) {
      kakao.maps.event.addListener(marker, 'mouseover', function () {
        displayInfowindow(marker, title);
      });

      kakao.maps.event.addListener(marker, 'mouseout', function () {
        infowindow.close();
      });

      itemEl.onmouseover = function () {
        displayInfowindow(marker, title);
      };

      itemEl.onmouseout = function () {
        infowindow.close();
      };
    })(marker, places[i].place_name);

    fragment.appendChild(itemEl);
  }

  listEl.appendChild(fragment);
  menuEl.scrollTop = 0;
  map.setBounds(bounds);
};

const getListItem = (index, places) => {
  const el = document.createElement('li');
  let itemStr = `<span class="markerbg marker_${index + 1}"></span>
                <div class="info">
                <h5>${places.place_name}</h5>`;

  if (places.road_address_name) {
    itemStr += `<span>${places.road_address_name}</span>
                <span class="jibun gray">${places.address_name}</span>`;
  } else {
    itemStr += `<span>${places.address_name}</span>`;
  }

  itemStr += `<span class="tel">${places.phone}</span></div><hr>`;

  el.innerHTML = itemStr;
  el.className = 'item';

  return el;
};

const addMarker = (position, idx) => {
  const imageSrc =
    'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png';
  const imageSize = new kakao.maps.Size(36, 37);
  const imgOptions = {
    spriteSize: new kakao.maps.Size(36, 691),
    spriteOrigin: new kakao.maps.Point(0, idx * 46 + 10),
    offset: new kakao.maps.Point(13, 37),
  };
  const markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
  const marker = new kakao.maps.Marker({
    position: position,
    image: markerImage,
  });

  marker.setMap(map);
  markers.value.push(marker);

  return marker;
};

const removeMarker = () => {
  for (let i = 0; i < markers.value.length; i++) {
    markers.value[i].setMap(null);
  }
  markers.value = [];
};

const displayPagination = (pagination) => {
  const paginationEl = document.getElementById('pagination');
  const fragment = document.createDocumentFragment();

  while (paginationEl.hasChildNodes()) {
    paginationEl.removeChild(paginationEl.lastChild);
  }

  for (let i = 1; i <= pagination.last; i++) {
    const el = document.createElement('a');
    el.href = '#';
    el.innerHTML = i;

    if (i === pagination.current) {
      el.className = 'on';
    } else {
      el.onclick = (function (i) {
        return function () {
          pagination.gotoPage(i);
        };
      })(i);
    }

    fragment.appendChild(el);
  }
  paginationEl.appendChild(fragment);
};

const displayInfowindow = (marker, title) => {
  const content = `<div style="padding:5px;z-index:1;">${title}</div>`;
  infowindow.setContent(content);
  infowindow.open(map, marker);
};

const removeAllChildNods = (el) => {
  while (el.hasChildNodes()) {
    el.removeChild(el.lastChild);
  }
};

onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    initMap();
  } else {
    const script = document.createElement('script');
    script.onload = () => kakao.maps.load(initMap);
    script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${import.meta.env.VITE_KAKAO_MAPS_API_KEY}&libraries=services`;
    document.head.appendChild(script);
  }
});
</script>

<style scoped>
#blackContainer {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #000000c7;
  z-index: 0;
}

#title {
  position: absolute;
  top: 100px; /* Adjusted top position to move title down */
  left: 150px;
  color: white;
  font-size: 30px;
  z-index: 2;
}

.map_wrap {
  position: absolute;
  top: 200px; /* Adjusted top position to move map down */
  left: 0;
  width: 100%;
  height: 600px; /* Increased height for better visibility */
  z-index: 1;
}

.map_wrap,
.map_wrap * {
  margin: 0;
  padding: 0;
  font-family: 'Malgun Gothic', dotum, '돋움', sans-serif;
  font-size: 12px;
}

.map_wrap a,
.map_wrap a:hover,
.map_wrap a:active {
  color: #000;
  text-decoration: none;
}

#map {
  width: 100%;
  height: 100%;
  top: 50px;
  position: absolute;
  overflow: hidden;
  z-index: 1;
}

#menu_wrap {
  position: absolute;
  top: 50px;
  left: 10px;
  width: 250px;
  height: 500px;
  margin: 10px 0 30px 10px;
  padding: 10px;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.9);
  z-index: 2;
  font-size: 12px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.bg_white {
  background: #fff;
}

#menu_wrap hr {
  display: block;
  height: 1px;
  border: 0;
  border-top: 2px solid #5f5f5f;
  margin: 10px 0;
}

#menu_wrap .option {
  text-align: center;
}

#menu_wrap .option p {
  margin: 10px 0;
}

#menu_wrap .option button {
  margin-top: 10px;
  margin-left: 5px;
  padding: 5px 10px;
  border: 1px solid black;
  border-radius: 5px;
  background: linear-gradient(-45deg, #8e44ad 0%, #c0392b 100%);
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s;
}

#menu_wrap .option button:hover {
  background-color: #0056b3;
}

#placesList {
  list-style: none;
  padding: 0;
  margin: 0;
}

#placesList .item {
  position: relative;
  border-bottom: 1px solid #ddd;
  overflow: hidden;
  cursor: pointer;
  min-height: 65px;
  background-color: #f9f9f9;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 5px;
  transition: background-color 0.3s, transform 0.3s;
}

#placesList .item:hover {
  background-color: #e9e9e9;
  transform: translateY(-2px);
}

#placesList .item span {
  display: block;
  margin-top: 4px;
}

#placesList .item h5,
#placesList .item .info {
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

#placesList .item .info {
  padding: 10px 0 10px 55px;
}

#placesList .info .gray {
  color: #8a8a8a;
}

#placesList .info .jibun {
  padding-left: 26px;
  background: url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_jibun.png)
    no-repeat;
}

#placesList .info .tel {
  color: #009900;
}

#placesList .item .markerbg {
  float: left;
  position: absolute;
  width: 36px;
  height: 37px;
  margin: 10px 0 0 10px;
  background: url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png)
    no-repeat;
}

#placesList .item .marker_1 {
  background-position: 0 -10px;
}

#placesList .item .marker_2 {
  background-position: 0 -56px;
}

#placesList .item .marker_3 {
  background-position: 0 -102px;
}

#placesList .item .marker_4 {
  background-position: 0 -148px;
}

#placesList .item .marker_5 {
  background-position: 0 -194px;
}

#placesList .item .marker_6 {
  background-position: 0 -240px;
}

#placesList .item .marker_7 {
  background-position: 0 -286px;
}

#placesList .item .marker_8 {
  background-position: 0 -332px;
}

#placesList .item .marker_9 {
  background-position: 0 -378px;
}

#placesList .item .marker_10 {
  background-position: 0 -423px;
}

#placesList .item .marker_11 {
  background-position: 0 -470px;
}

#placesList .item .marker_12 {
  background-position: 0 -516px;
}

#placesList .item .marker_13 {
  background-position: 0 -562px;
}

#placesList .item .marker_14 {
  background-position: 0 -608px;
}

#placesList .item .marker_15 {
  background-position: 0 -654px;
}

#pagination {
  margin: 10px auto;
  text-align: center;
}

#pagination a {
  display: inline-block;
  margin-right: 10px;
  padding: 5px 10px;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  transition: background-color 0.3s;
}

#pagination a:hover {
  background-color: #0056b3;
}

#pagination .on {
  font-weight: bold;
  cursor: default;
  color: #777;
  background-color: #e9e9e9;
}

</style>
