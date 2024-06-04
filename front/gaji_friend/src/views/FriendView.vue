<template>
  <div>
    <div id="blackContainer"></div>
     <div id="links">
      <div>
        <RouterLink :to="{ name: 'friend_list' }">친구 목록</RouterLink>
      </div>
      <div>
        <RouterLink :to="{ name: 'friend_search' }">친구 찾기</RouterLink>
      </div>
      <div>
        <RouterLink :to="{ name: 'theater' }">근처 영화관</RouterLink>
      </div>
    </div>
    <div>
      <h1>🎁추천친구 목록입니다.</h1>
      <div id="friendRec">
        <carousel :items-to-show="6" :itemsToScroll="5" :transition="400">
          <slide v-for="user in filteredUsers" :key="user.pk">
              <div 
              id="one-friend" 
              @mouseenter="moveUp(user)"
              @mouseleave="moveDown(user)"
              :class="{ 'selected': isSelected[user.pk]}"
              >
                <div id="image">
                  <img :src="`http://127.0.0.1:8000${user.image}`" alt="프로필 사진" />
                  <!-- <img
                    :src="`http://127.0.0.1:8000/${user.image}`"
                    alt="프로필 사진"
                  /> -->
                </div>
                <div class="divider"></div>
                <div id="info-container">
                  <div id="nickname">{{ user.nickname }}</div>
                    <div id="details">
                      <div id="gender">{{ user.gender }}</div>
                      <div id="location">{{ user.location }}</div>
                      <div id="liked-genre">{{ user.genre }}</div>
                    </div>
                </div>
                <button @click="toggleFollow(user.pk)">
                  {{ followButtonText(user.pk) }}
                </button>
              </div>
          </slide>
          <template #addons>
            <Navigation />
          </template>
        </carousel>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { RouterLink } from "vue-router";
import { useCommunityStore } from "@/stores/community";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import "vue3-carousel/dist/carousel.css";
import { Carousel, Slide, Pagination, Navigation } from "vue3-carousel";

const users = useAuthStore();
const userInfo = users.userdetail;
const token = ref(null);
const API_URL = "http://127.0.0.1:8000";

onMounted(() => {
  token.value = users.token; // 마운트 후 토큰 할당
  userInfo.value = users.userdetail;
});

const communityStore = useCommunityStore();
onMounted(() => {
  communityStore.getusers();
});

const userslist = ref(communityStore.users); // 반응성 데이터 소스
const searchGenre = ref("");
const filteredUsers = computed(() => {
  // userInfo에 현재 로그인한 사용자의 정보가 저장되어 있고,
  // userslist에는 로그인하지 않은 사용자 목록이 있어야 합니다.
  return userslist.value.filter(
    (user) =>
      // 로그인한 유저와 다른 유저를 비교
      // user.pk !== userInfo.pk &&
      // // 같은 장르를 선호하는지 확인
      // user.genre === userInfo.genre ||
      user.pk !== userInfo.pk &&
      user.location.split(" ")[0] === userInfo.location.split(" ")[0]
  );
});

// 각 사용자의 팔로우 상태를 저장하는 객체
const followStatus = ref({});

// 사용자의 초기 팔로우 상태를 설정하는 함수
const setInitialFollowStatus = () => {
  filteredUsers.value.forEach((user) => {
    followStatus.value[user.pk] = userInfo.followings.includes(user.pk); // userInfo.followings에 포함되어 있는지 확인
  });
};

watch(filteredUsers, setInitialFollowStatus, { immediate: true });

const toggleFollow = async (userId) => {
  try {
    const response = await axios({
      method: "post",
      url: `${API_URL}/api/v1/user/follow/${userId}/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    });

    if (response.data.status === "success") {
      console.log("팔로우 상태가 변경되었습니다.");
      followStatus.value[userId] = !followStatus.value[userId];

      if (followStatus.value[userId]) {
        userInfo.followings.push(userId); // 팔로우 추가
      } else {
        userInfo.followings = userInfo.followings.filter((id) => id !== userId); // 팔로우 제거
      }
    }
  } catch (error) {
    console.error("팔로우 처리 중 오류가 발생했습니다.", error);
  }
};

const followButtonText = (userId) => {
  return followStatus.value[userId] ? "언팔로우" : "팔로우";
};

const searchFriends = () => {
  if (searchGenre.value) {
    filteredUsers.value = userslist.value.filter((user) =>
      user.genre.includes(searchGenre.value)
    );
  } else {
    filteredUsers.value = userslist.value;
  }
};

const isSelected = ref({})

const moveUp = function(user) {
  isSelected.value[user.pk] = true
}

const moveDown = function(user) {
  isSelected.value[user.pk] = false
}

// 페이지 이동 함수
// const scrollLeft = () => {
//   const carousel = document.querySelector('.carousel');
//   carousel.scrollBy({
//     left: -300,
//     behavior: 'smooth'
//   });
// };

// const scrollRight = () => {
//   const carousel = document.querySelector('.carousel');
//   carousel.scrollBy({
//     left: 300,
//     behavior: 'smooth'
//   });
// };

// const currentPage = ref(0);
// const itemsPerPage = 5;

// const paginatedUsers = computed(() => {
//   const start = currentPage.value * itemsPerPage;
//   const end = start + itemsPerPage;
//   return filteredUsers.value.slice(start, end);
// });

// const scrollLeft = () => {
//   if (currentPage.value > 0) {
//     currentPage.value--;
//   }
// };

// const scrollRight = () => {
//   if (currentPage.value < Math.ceil(filteredUsers.value.length / itemsPerPage) - 1) {
//     currentPage.value++;
//   }
// };
</script>

<style scoped>
#blackContainer {
  position: fixed;
  width: 2000px;
  height: 1000px;
  background-color: #000000c7;
  z-index: 0;
}

#links {
  display: flex;
  position: absolute;
  top: 190px;
  left: 650px;
  z-index: 1;
}

#links > * {
  margin: 0 60px;
  text-align: center;
  width: 110px;
  height: 35px;
  border: 2px solid #56778b95;
  border-radius: 5%;
}

#links > div {
  background: rgba(82, 82, 82, 0.467);
}
#links > div > a {
  text-decoration: none;
  color: white;
}

h1 {
  position: absolute;
  top: 285px;
  left: 200px;
  color: #ffffff;
  text-shadow: 2px 3px 10px #7E8C95;
  z-index: 1;
}

#friendRec {
  position: absolute;
  width: 1900px;
  height: 700px;
  top: 210px;
  display: flex;
  align-items: flex-end;
}


#one-friend {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid black;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 350px;
  height: 500px;
  margin: 10px;
  overflow: hidden;
  background-color: rgb(255, 255, 255);
  transition: transform 0.2s;
  
}
/* 페이지 이동 스타일 */

.carousel::-webkit-scrollbar {
  display: none;
}

.carousel__prev,
.carousel__next {
  box-sizing: content-box;
  border: 5px solid white;
}

.carousel {
  display: flex;
  overflow-x: hidden;
  scroll-behavior: smooth;
  -ms-overflow-style: none;
  scrollbar-width: none; 
}

.carousel-container {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 1s;
}

.selected {
  position: absolute;
  transition: transform 0.5s ease;
  transform: translateY(-20px);
}

.selected:hover {
  transform: translateY(-5px);
}

#image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

#image img {
  width: 100%;
  height: 100%;
}

#info-container {
  display: flex;
  flex-direction: column;
  padding: 10px;
}

#nickname {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}

#details {
  justify-content: space-between;
  margin-bottom: 10px;
}

#gender,
#location {
  font-size: 1em;
}

#one-liner,
#liked-genre {
  font-size: 0.9em;
  padding: 10px;
  text-align: center;
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


.divider {
  width: 80%;
  height: 1px;
  background-color: #000000;
  margin: 10px 0;
}

#main-image {
  width: 100%;
  height: 300px;
  background-size: cover;
  background-position: top;
} 
</style>
