```javascript
<template>
  <div>
    <div id="blackContainer"></div>
    <h1 id="title">🔊최신영화</h1>
    <div id="carouselContainer">
      <!-- {{ movieList }} -->
      <carousel
        :autoplay="10"
        :pauseAutoplayOnHover="true"
        :wrapAround="true"
        :transition="2500"
        :itemsToScroll="2"
        :items-to-show="4"
        :per-page="4"
        navigation-enabled
        navigation-dots-enabled
      >
        <Slide v-for="newMovie in movieList" :key="newMovie.id">
          <MovieDetail
            :newMovie="newMovie"
            @click="openModal(newMovie)"
            id="poster"
          />
        </Slide>
        <template #addons>
          <navigation>
            <template #next>
              <span id="next_ca">>></span>
            </template>
            <template #prev>
              <span id="prev_ca"><<</span>
            </template>
          </navigation>
        </template>
      </carousel>
    </div>
    <div id="blackModal" v-if="modalActive" @click="closeModal"></div>
    <div id="modalContainer" v-if="modalActive">
      <p id="close" @click="closeModal">❌</p>
      <div id="modal">
        <div id="modalContent">
          <img
            :src="image_url + selectedMovie.poster_path"
            :alt="selectedMovie.poster_path"
            id="movieposter"
          />
          <div id="modalInfo">
            <h2>제목 : {{ selectedMovie.title }}</h2>
            <p>장르 : {{ selectedMovie.genres }}</p>
            <p>개봉일 : {{ selectedMovie.release_date.slice(0, 10) }}</p>
            <p>평점 : {{ selectedMovie.vote_average }}</p>
            <p>
              줄거리 <br />
              {{ selectedMovie.overview }}
            </p>
            <div class="movie-info">
              <iframe
                v-if="movieId"
                :src="`https://www.youtube.com/embed/${movieId}`"
                width="560"
                height="315"
                allowfullscreen
              ></iframe>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="black"></div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useCounterStore } from "@/stores/movie";
import MovieDetail from "@/components/MovieDetail.vue";
import axios from "axios";
import "vue3-carousel/dist/carousel.css";
import { Carousel, Slide, Pagination, Navigation } from "vue3-carousel";
const store = useCounterStore();
const image_url = "https://image.tmdb.org/t/p/w300/";

const modalActive = ref(false);
const selectedMovie = ref({});
const currentPage = ref(1);
const pageSize = 4;
const totalPages = computed(() => Math.ceil(store.newMovies.length / pageSize));
const displayedMovies = ref([]);
const movieId = ref(null);
const API_KEY = import.meta.env.VITE_YOU_TUBE_API_KEY2;
const movieList = ref([]);

onMounted(() => {
  store.getNewMovies();
  fetchMovies();
  movieList.value = store.newMovies;
});

function fetchMovies() {
  const start = (currentPage.value - 1) * pageSize;
  const end = currentPage.value * pageSize;
  displayedMovies.value = store.newMovies.slice(start, end);
}

function openModal(newMovie) {
  modalActive.value = true;
  selectedMovie.value = newMovie;
}

function closeModal() {
  modalActive.value = false;
  selectedMovie.value = {}; // 모달을 닫을 때 선택된 영화 초기화
  movieId.value = null; // 모달을 닫을 때 영화 예고편 초기화
}

const nextPage = function () {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    fetchMovies();
  }
};

function go_previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
    fetchMovies();
  }
}

// 영화 예고편
watch(selectedMovie, (newVal) => {
  if (newVal && newVal.title) {
    onSearchMovie(newVal.title);
  }
});

function onSearchMovie(movieTitle) {
  axios({
    method: "get",
    url: `https://www.googleapis.com/youtube/v3/search?key=${API_KEY}`,
    params: {
      part: "snippet",
      type: "video",
      q: movieTitle + "예고편", // 영화 제목 + 트레일러
    },
  })
    .then((response) => {
      if (
        response.data.items.length > 0 &&
        response.data.items[0].snippet.title.includes(movieTitle)
      ) {
        console.log(response.data.items[0].snippet.title);
        console.log(movieTitle);
        movieId.value = response.data.items[0].id.videoId;
      } else {
        movieId.value = null;
        console.log("No trailers found for this movie");
      }
    })
    .catch((error) => {
      console.log(error);
    });
}
</script>

<style scoped>
/* CSS 스타일은 중복되는 부분을 제거하고 필요한 스타일만 남겨 두었습니다. */
#blackContainer,
#blackModal,
#black {
  position: fixed;
  width: 100%;
  height: 100%;
  background-color: #000000c7;
  opacity: 0.5;
  z-index: 0;
  transition-duration: 2.5s;
}

#title {
  position: absolute;
  left: 240px;
  top: 155px;
  color: #ffffff;
  text-shadow: 3px 3px 5px #7e8c95;
  z-index: 1;
}
.carousel {
  /* background-color: blue; */
  padding: auto;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 1600px;
  height: 100%;
  overflow-x: hidden;
  scroll-behavior: smooth;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

#carousel-card {
  /* background: blue; */
  margin: 10px;
  height: 1000px;
}

#carouselContainer,
#modalContainer {
  position: absolute;
  display: flex;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
}

#poster {
  margin: 0 10px;
  z-index: 1;
  border: solid black 1px;
  border-radius: 10px; /* 모서리를 둥글게 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 2); /* 그림자 효과 */
}

#poster:hover {
  transform: translateY(-10px);
}

#movieposter {
  width: 300px; /* Set your desired width */
  height: 500px;
  object-fit: cover; /* 이미지가 컨테이너를 완전히 덮도록 설정 */
  border: 10px solid black; /* 2px 두께의 검은색 테두리 추가 */
  border-radius: 50px; /* 둥근 테두리를 원한다면, 이 값을 설정 */
}

#modal {
  width: 1200px;
  height: 700px;
  border-radius: 20px;
  background-color: rgba(0, 31, 63, 0.95); /* 반투명 흰색 배경 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* 더 강한 그림자 */
  border: 1px solid #444; /* 진한 회색 테두리 */
  z-index: 2;
  padding: 20px; /* 내부 여백 */
  color: #f1f1f1; /* 밝은 텍스트 색상 */
}
/* #modal {
  width: 1200px;
  height: 700px;
  border-radius: 20px;
  background-color: #b2c5d1;
  box-shadow: 2px 3px 5px 0px rgb(36, 36, 36);
  z-index: 2;
} */

#modal img {
  margin-right: 20px;
}
#modalContent {
  display: flex;
  margin-top: 20px;
  margin-left: 20px;
  z-index: 2;
}

#modalInfo {
  z-index: 2;
}

#close {
  position: fixed;
  top: 10px;
  left: 1130px;
  z-index: 4;
  /* background-color: #6c757d; 부드러운 회색 */
  color: #f9f9f9; /* 텍스트 색상 */
  border: none; /* 테두리 제거 */
  padding: 10px 20px; /* 여백 추가 */
  border-radius: 5px; /* 둥근 모서리 */
  transition: background-color 0.3s;
}

#close:hover {
  background-color: #2fb1e4; /* 부드러운 회색 톤으로 변경 */
}

.pagination-container {
  display: flex;
  justify-content: center;
  z-index: 1000;
}

.prev,
.next {
  background-color: transparent;
  border: none;
  font-size: 4em;
  cursor: pointer;
  position: absolute;
  top: 470px;
  transform: translateY(-50%);
  z-index: 1;
}

/* .prev {
  left: 230px;
}
.next {
  left: 1605px;
} */

button {
  margin: 10px;
  padding: 8px 16px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #7e8c95;
  cursor: pointer;
  transition: background-color 0.3s;
  z-index: 1;
}

button:hover {
  background-color: #0056b3;
}
</style>