<template>
  <div>
    <div id="blackContainer"></div>
    <p id="user">🔒{{ userInfo.nickname }}님 프로필</p>
     <div id="profile">
        <div id="info">
          <img :src="userInfo.image ? userInfo.image : 'http://127.0.0.1:8000/media/users/default.png'" alt="User Image">
          <p id="nickname">{{ userInfo.nickname }}</p>
          <p id="age">나이 : {{ userInfo.age }}</p>
          <p id="genre">선호 장르 : {{ userInfo.genre }}</p>
          <p id="gender">성별 : {{ userInfo.gender }}</p>
          <p id="location">지역 : {{ userInfo.location }}</p>
          <p id="friend">친구 수 : {{ userInfo.followings.length }}</p>
          <input type="file" @change="uploadImage" accept="image/*" />
        </div>
         <div v-if="myLikeMovieList.length" id="movies">
          <h2>좋아요 누른 영화들</h2>
          <div id="movieList">
            <ul>
              <li v-for="movie in myLikeMovieList" :key="movie.id" id="oneMovie">
                <img :src="image_url + movie.poster_path" :alt="movie.title" />
                <div id="movieText">
                  <h4>{{ movie.title }}</h4>
                  <p>평점 : {{ movie.vote_average }}</p>
                  <p>[줄거리]</p>
                  <p>{{ movie.overview }}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <div v-else>
          <p>좋아요 누른 영화가 없습니다.</p>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth';
import axios from 'axios'

const store = useAuthStore()
const myLikeMovieList = ref([])
const image_url = 'https://image.tmdb.org/t/p/w300/'
const token = ref(store.token) 
const userInfo = ref(store.userdetail)

// const defaultImage = 'http://127.0.0.1:8000/media/users/defalult.png';

// const imageSrc = computed(() => {
//   return userInfo.value.image | defaultImage;
// });

// function setDefaultImage(event) {
//   event.target.src = defaultImage;
// }

onMounted(() => {
  store.userDetail()
  getLikedMovies()
})

const uploadImage = async (event) => {
  const file = event.target.files[0]
  if (!file) return;

  const formData = new FormData();
  formData.append('image', file);

  try {
    const response = await axios({
      method: 'put',
      url: 'http://127.0.0.1:8000/api/v1/user/profile/',
      data: formData,
      headers: {
        'Authorization': `Token ${token.value}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    userInfo.value.image = response.data.image; // 서버로부터 받은 이미지 URL 업데이트

  } catch (error) {
    console.error('Error uploading image:', error);
  }
}

const getLikedMovies = function () {
  axios({
    method: 'get',
    url: `http://127.0.0.1:8000/api/v1/user/liked/`,
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
  .then(response => {
    myLikeMovieList.value = response.data
  })
  .catch(error => {
    console.error('좋아요 누른 영화를 불러오는 중 오류가 발생했습니다.', error)
  })
}
</script>

<style scoped>
#blackContainer {
  position: fixed;
  width: 2000px;
  height: 1000px;
  background-color: #000000cf;
  z-index: 0;
}

* {
  font-family: "Jua", sans-serif;
  font-weight: 400;
  font-style: normal;
  z-index: 1;
  
}

#user {
  position: absolute;
  font-size: 26px;
  top: 83px;
  left: 110px;
  color: white;
  
}

#profile {
  position: absolute;
  display: flex;
  left: 1px;
  top: 145px;
  color: white
}

#info {
  border: 1px solid black;
  border-radius: 30px;
  background-color: rgba(10, 27, 45, 0.95);
  height: 675px;
  width: 530px;
  left: 140x;
  margin-left: 150px;
  margin-right: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

#movies {
  position: absolute;
  height: 700px;
  width: 1160px;
  top: -9px;
  left: 762px;
  margin-top: -10px;
  margin-left: -66px;
}

#info > img {
  border: 2px solid black;
  border-radius: 50%;
  width: 240px;
  height: 240px;
  margin-top: 25px;
}

#info > #nickname {
  margin-top: 20px;
  font-size: 36px;
}

#info > #age {
  margin-bottom: 0;
  margin-top: 36px;
  font-size: 20px;
}

#info > #genre, #info > #gender, #info > #location, #info > #friend {
  margin-top: 1px;
  margin-bottom: 0;
  font-size: 20px;
}

#info > #friend {
  margin-bottom: 70px;
}

#movieList {
  position: absolute;
  height: 660px;
  width: 1160px;
  overflow-y: auto;
}

#movieList::-webkit-scrollbar {
  width: 5px;
}

#movieList::-webkit-scrollbar-thumb {
  height: 0.5px;
  background: #F2D8D5;
  border-radius: 10px;
}

#movieList::-webkit-scrollbar-track {
  background-color: #BFB6AE;
}

#oneMovie {
  width: 1100px;
  margin: 25px 0;
}

#movieText {
  margin: 10px 0 0 20px;
}

li {
  display: flex;
  width: 800px;
  height: 275px;
}

</style>