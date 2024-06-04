<template>
  <div id="blackContainer"></div>
  <div id="maincontainer">
    <div id="black-change" v-if="isModal" @click="closeModal"></div>
    <div id="title-container">
      <p id="user-name">
        {{ userInfo.nickname }}님이 좋아하는 장르: {{ userInfo.genre }}
        <span><button @click="changeTopRatedMovies">최고 평점</button></span>
        <span><button @click="changefilteredMovies">장르</button></span>
      </p>
    </div>
    <div id="contentcontainer">
      <div v-if="filteredMovies.length">
        <p id="title">🔔추천 영화</p>
        <div id="movieContainer">
          <carousel
            :wrapAround="true"
            :transition="700"
            :itemsToScroll="3"
            :items-to-show="4"
            :per-page="4"
            navigation-enabled
            navigation-dots-enabled
          >
            <slide
              v-for="movie in filteredMovies"
              :key="movie.id"
              id="carousel-card"
            >
              <div id="per-movie">
                <img
                  :src="image_url + movie.poster_path"
                  :alt="movie.title"
                  @click.stop="makeModal(movie)"
                  class="d-block w-100"
                  id="poster"
                />
                <div>
                  <button
                    id="liked"
                    @click.stop="toggleLike(movie.id)"
                    class="like-button"
                  >
                    {{ isLiked[movie.id] ? "💗" : "🖤" }}
                  </button>
                </div>
              </div>
            </slide>
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
      </div>
    </div>
    <div id="modal-container" v-if="isModal">
      <div id="modal">
        <div id="modal-content">
          <p @click="closeModal" id="closed">❌</p>
          <img
            :src="image_url + selectedMovie.poster_path"
            alt=""
            id="movieposter"
          />
          <div id="modal-text">
            <p>제목 : {{ selectedMovie.title }}</p>
            <p>장르 : {{ selectedMovie.genres }}</p>
            <p>평점 : {{ selectedMovie.vote_average }}</p>
            <p>개봉일 : {{ selectedMovie.release_date.slice(0, 10) }}</p>
            <p>줄거리 <br />{{ selectedMovie.overview }}</p>
            <p>
              좋아요를 누른 사람 수 : {{ selectedMovie.like_users.length }}명
            </p>
            <p v-if="selectedMovie.is_liked">💗</p>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useCounterStore } from "@/stores/movie";
import axios from "axios";
import "vue3-carousel/dist/carousel.css";
import { Carousel, Slide, Pagination, Navigation } from "vue3-carousel";

const API_KEY = import.meta.env.VITE_YOU_TUBE_API_KEY2;
const userStore = useAuthStore();
const movieStore = useCounterStore();
const userInfo = ref([]);
const movieList = ref([]);
const isLiked = ref({});
const image_url = "https://image.tmdb.org/t/p/w300/";
const API_URL = "http://127.0.0.1:8000";
const currentPage = ref(1);
const moviesPerPage = 4;
const isModal = ref(false);
const selectedMovie = ref(null);
const token = ref(null);
const movieId = ref(null); // Added movieId to hold the trailer video ID
userInfo.value = userStore.userdetail;
let filteredMovies = ref([]);
onMounted(async () => {
  movieStore.getMovies();
  movieList.value = movieStore.Movies;
  initializeLikes();
  token.value = userStore.token;
  changefilteredMovies();
});

// Watch for changes in selectedMovie to fetch the trailer
watch(selectedMovie, (newVal) => {
  if (newVal && newVal.title) {
    onSearchMovie(newVal.title);
  }
});

// Function to fetch the trailer from YouTube
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

function initializeLikes() {
  movieList.value.forEach((movie) => {
    isLiked.value[movie.id] = movie.like_users.includes(userInfo.value.pk);
  });
}

const toggleLike = async (movieId) => {
  const liked = isLiked.value[movieId];
  try {
    await axios.post(
      `${API_URL}/api/v1/movies/${movieId}/like/`,
      {},
      {
        headers: { Authorization: `Token ${token.value}` },
      }
    );
    isLiked.value[movieId] = !liked;
  } catch (error) {
    console.error("Error toggling like:", error);
  }
};

const filteredMoviesGenre = computed(() => {
  return movieList.value.filter((movie) =>
    movie.genres.includes(userInfo.value.genre)
  );
});

const filteredMoviesTop = computed(() => {
  return movieList.value
    .slice() // 원본 배열의 복사본을 생성
    .sort((a, b) => b.vote_average - a.vote_average) // vote_average를 기준으로 내림차순 정렬
    .slice(0, 30); // 상위 30개의 영화만 반환
});

const changefilteredMovies = () => {
  filteredMovies.value = filteredMoviesGenre.value;
};

const changeTopRatedMovies = () => {
  filteredMovies.value = filteredMoviesTop.value;
};

const currentPageData = computed(() => {
  const start = (currentPage.value - 1) * moviesPerPage;
  return filteredMovies.value.slice(start, start + moviesPerPage);
});

const totalPages = computed(() =>
  Math.ceil(filteredMovies.value.length / moviesPerPage)
);

const previousPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const makeModal = (movie) => {
  selectedMovie.value = movie;
  isModal.value = true;
};

const closeModal = () => {
  isModal.value = false;
  movieId.value = null; // Reset the trailer when modal is closed
};

watch(
  () => isLiked.value,
  () => {
    initializeLikes();
  }
);
</script>

<style scoped>
#blackContainer {
  position: fixed;
  width: 2000px;
  height: 1000px;
  background-color: #000000c7;
  z-index: 0;
}

#maincontainer {
  display: flex;
  flex-direction: column;
  position: fixed;
  width: 100vw;
  height: 100vh;
  font-family: "Jua", sans-serif;
  font-weight: 400;
  font-style: normal;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

#movieContainer {
  position: absolute;
  display: flex;
  top: 55%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.contentcontainer {
  position: absolute;
  left: 10px;
  background-color: rgb(185, 11, 11);
}

#next_ca {
  /* background-color: white; */
  font-size: 50px;
  position: absolute;
  height: 100px;
  justify-content: center;
  align-items: center;
  top: 250px;
  right: 650px;
  color: white;
}

#prev_ca {
  font-size: 50px;
  position: absolute;
  height: 100px;
  justify-content: center;
  align-items: center;
  top: 250px;
  left: 650px;
  color: white;
}

#title-container,
#title {
  text-shadow: 3px 3px 10px #7e8c95;
}

.carousel {
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
  margin: 5px;
  height: 1000px;
}

#title-container {
  position: absolute;
  left: 130px;
  top: 100px;
  color: #f2d8d5;
  font-size: 35px;
  z-index: 1;
}

#title {
  position: absolute;
  left: 130px;
  top: 160px;
  color: #f2d8d5;
  font-size: 30px;
  z-index: 1;
}

#per-movie {
  position: relative;
  z-index: 1;
}

#poster {
  border-radius: 10px; /* 모서리를 둥글게 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 2); /* 그림자 효과 */
}

#poster:hover {
  transform: translateY(-10px);
}

ul {
  display: flex;
  position: relative;
  top: 180px;
  left: 100px;
}

ul > * {
  margin: 0 10px;
}

#modal-container {
  display: flex;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -45%);
  border-radius: 30px;
  background-color: rgba(0, 31, 63, 0.8); /* 반투명 흰색 배경 */
  width: 1100px;
  height: 800px;
  align-items: center;
  justify-content: center;
  z-index: 1;
}

#modal-content {
  display: flex;
  width: 100%;
  height: 100%;
  margin-top: 50px;
}

#modal-content > img {
  margin-left: 40px;
}

#black-change {
  position: fixed;
  display: fixed;
  width: 100%;
  height: 100%;
  background: #000000d0;
  z-index: 1;
}

#modal-text {
  color: whitesmoke;
  margin: 0 15px;
}

#closed {
  position: fixed;
  top: 15px;
  left: 930px;
}

.like-button {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 24px;
  padding: 5px;
}

.like-button:hover {
  background-color: #f0f0f0; /* 예시: 호버 시 배경색 변경 */
  border-radius: 5px; /* 버튼 모서리를 둥글게 */
}

/* 페이지 이동 스타일 */
.prev,
.next {
  background-color: transparent;
  border: none;
  font-size: 4em;
  cursor: pointer;
  position: absolute;
  top: 40%;
  transform: translateY(-50%);
}

.prev {
  left: -50px;
}

.next {
  right: 130px;
}

button {
  display: inline-block;
  margin: 10px;
  padding: 8px 16px;
  font-size: 14px;
  border: 1px solid black;
  border-radius: 5px;
  background: linear-gradient(-45deg, #8e44ad 0%, #c0392b 100%);
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background: linear-gradient(-45deg, #bab7bb 0%, #c0392b 100%);
}
#movieposter {
  width: 300px; /* Set your desired width */
  height: 400px;
  margin-top: 50px;
  object-fit: cover; /* 이미지가 컨테이너를 완전히 덮도록 설정 */
  border: 5px solid black; /* 2px 두께의 검은색 테두리 추가 */
  border-radius: 50px; /* 둥근 테두리를 원한다면, 이 값을 설정 */
}

#closed {
  margin-left: 100px;
}
</style>
