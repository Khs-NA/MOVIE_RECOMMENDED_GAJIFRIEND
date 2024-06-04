<template>
  <div id="container">
    <div id="image">
      <img :src="`http://127.0.0.1:8000${friend.image}`" alt="프로필 사진" />
    </div>
    <div id="text">
      <div id="nickname">{{ friend.nickname }}</div>
      <div id="overview">{{ friend.name }}</div>
      <div id="details">{{ friend.age }}세, {{ friend.gender }}</div>
      <div id="details">{{ friend.location }}</div>
      <div id="follow_friend">
        <button @click="toggleFollow(friend.pk)">{{ followButtonText(friend.pk) }}</button>    
      </div>
    </div>
      <div id="like_movie">
        <ul>
          <h4 id="title">선호하는 영화</h4>
          <template v-if="likeMovies.length > 0">
            <li v-for="movie in likeMovies" :key="movie.id">
              {{ movie.title }}
            </li>
          </template>
          <li v-else>
            아직까지 선호하는 영화가 없습니다.
          </li>
        </ul>
      </div>
  </div>
</template>

<script setup>
import { defineProps, ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useCounterStore } from '@/stores/movie';


const props = defineProps({
  friend: {
    type: Object,
    required: true
  }
});

const movies = useCounterStore()
const users = useAuthStore();
const MovieInfo = movies.Movies;
const userInfo = users.userdetail;
const token = ref(null);
const API_URL = 'http://127.0.0.1:8000';

onMounted(() => {
  token.value = users.token; // 마운트 후 토큰 할당
  userInfo.value = users.userdetail;
  MovieInfo.value = movies.Movies
  setInitialFollowStatus(); // 초기 팔로우 상태 설정
  LikeMoviesCheck()
  movies.getMovies()
});

// 각 사용자의 팔로우 상태를 저장하는 객체
const followStatus = ref({});

// 사용자의 초기 팔로우 상태를 설정하는 함수
const setInitialFollowStatus = () => {
  followStatus.value[props.friend.pk] = userInfo.followings.includes(props.friend.pk);
};

const toggleFollow = async (userId) => {
  try {
    const response = await axios({
      method: 'post',
      url: `${API_URL}/api/v1/user/follow/${userId}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    });

    if (response.data.status === 'success') {
      console.log('팔로우 상태가 변경되었습니다.');
      followStatus.value[userId] = !followStatus.value[userId];

      if (followStatus.value[userId]) {
        userInfo.followings.push(userId); // 팔로우 추가
      } else {
        userInfo.followings = userInfo.followings.filter(id => id !== userId); // 팔로우 제거
      }
    }
  } catch (error) {
    console.error('팔로우 처리 중 오류가 발생했습니다.', error);
  }
};

const followButtonText = (userId) => {
  return followStatus.value[userId] ? '언팔로우' : '팔로우';
};


// 각 사용자가 좋아요 한 영화 리스트 보기
const likeMovies = ref({});

// 사용자의 초기 팔로우 상태를 설정하는 함수
const LikeMoviesCheck = () => {
  likeMovies.value = MovieInfo.filter(movie => 
      movie.like_users.includes(props.friend.pk)
  )
};




</script>

<style scoped>
#container {
  display: flex;
  border: 1px solid #ccc;
  border-radius: 10px;
  width: 48%;
  height: 300px;
  margin: 20px 100px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  background-color: #fff;
}

#container:hover {
  transform: scale(1.05);
}

#image {
  width: 30%;
  height: auto;
  overflow: hidden;
}

#image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
}

#text {
  width: 30%;
  padding: 20px;
  /* background-color: #f8f8f8; */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  /* align-items: flex-start; */
  /* border-right: 1px solid #eee; */
}

#like_movie {
  width: 40%;
  /* background-color: #f1f1f1; */
  padding: 20px;
  /* display: flex;
  flex-direction: column; */
  justify-content: center;
}

#nickname {
  font-weight: bold;
  font-size: 1.5em;
  color: #333;
  margin-bottom: 10px;
}

#overview, #details, #genre {
  margin-top: 5px;
  color: #666;
}

#title {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 10px;
  color: #333;
}

button {
  display: inline-block;
  margin: 10px;
  padding: 8px 16px;
  font-size: 14px;
  border: 0.5px solid black;
  border-radius: 5px;
  background: linear-gradient(-45deg, #8e44ad 0%, #c0392b 100%);
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #ff85c0;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}


</style>
