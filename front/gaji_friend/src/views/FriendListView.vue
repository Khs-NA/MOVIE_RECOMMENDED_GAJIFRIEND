<template>
  <div>
    <div id="blackContainer"></div>
    <h1>🧸친구 목록입니다.</h1>
    <div id="main-container">
      <carousel :items-to-show="6" :itemsToScroll="5" :transition="400">
        <slide v-for="user in filteredUsers" :key="user.pk">
          <div class="container">
            <div id="one-friend">
              <div id="image">
                <img :src="`http://127.0.0.1:8000${user.image}`" alt="프로필 사진" />
              </div>
              <div id="info-container">
                <div id="nickname">{{ user.nickname }}</div>
                <div id="details">
                  <div id="gender">{{ user.gender }}</div>
                  <div id="location">{{ user.location }}</div>
                  <div id="liked-genre">{{ user.genre }}</div>
                </div>
              </div>
              <div id="button">
                <button @click="toggleFollow(user.pk)">
                  {{ followButtonText(user.pk) }}
                </button>
                <button>채팅하기</button>
              </div>
            </div>
          </div>
        </slide>
        <template #addons>
          <navigation>
            <template #next>
              <span id="next_ca">>></span>
            </template>
            <template #prev>
              <span id="prev_ca"><< </span>
            </template>
          </navigation>
        </template>
      </carousel>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useCommunityStore } from "@/stores/community";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";
import { useRouter } from "vue-router";
import { Carousel, Slide, Pagination, Navigation } from "vue3-carousel";

const communityStore = useCommunityStore();
const users = useAuthStore();
const router = useRouter();
const userInfo = users.userdetail;
const userslist = ref(communityStore.users);
const token = ref(null);
const API_URL = "http://127.0.0.1:8000";

onMounted(() => {
  token.value = users.token; // 마운트 후 토큰 할당
  communityStore.getusers();
  userInfo.value = users.userdetail; // 유저 정보를 다시 로드
});

const filteredUsers = computed(() => {
  return userslist.value.filter(
    (user) => user.pk !== userInfo.pk && userInfo.followings.includes(user.pk)
  );
});

// 각 사용자의 팔로우 상태를 저장하는 객체
const followStatus = ref({});

// 사용자의 초기 팔로우 상태를 설정하는 함수
const setInitialFollowStatus = () => {
  userslist.value.forEach((user) => {
    followStatus.value[user.pk] = userInfo.followings.includes(user.pk); // userInfo.followings에 포함되어 있는지 확인
  });
};

watch(userslist, setInitialFollowStatus, { immediate: true });

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

</script>
<style scoped>
#blackContainer {
  position: fixed;
  width: 2000px;
  height: 1000px;
  background-color: #000000c7;
  z-index: 0;
}

h1 {
  position: absolute;
  top: 195px;
  left: 200px;
  color: #ffffff;
  text-shadow: 2px 2px 10px #7E8C95;
  z-index: 1;
}

#main-container {
  position: absolute;
  width: 1900px;
  height: 590px;
  top: 285px;
  display: flex;
  align-items: flex-end;
}

/* 페이지 이동 스타일 */

.carousel::-webkit-scrollbar {
  display: none;
  /* Chrome, Safari, Opera */
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
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

.carousel-container {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: transform 1s;
}

/* .prev,
.next {
  background-color: transparent;
  border: none;
  font-size: 2em;
  cursor: pointer;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 999;
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
} */

#one-friend {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid black;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 285px;
  height: 510px;
  margin: 10px;
  overflow: hidden;
  background-color: rgb(255, 255, 255);
  transition: transform 0.2s;
}

#one-friend:hover {
  transform: translateY(-5px);
}

#image {
  height: 220px;
  width: 100%;
  overflow: hidden;
}

#image img {
  object-fit: cover;
  height: 100%;
  width: 100%;
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
  /* display: flex; */
  justify-content: space-between;
  margin-bottom: 10px;
}

#gender,
#location {
  font-size: 1em;
}

#liked-genre {
  font-size: 0.9em;
  padding: 0px;
  text-align: center;
}

#button {
  padding-top: 30px;
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
  background-color: #0056b3;
}

.divider {
  width: 80%;
  height: 1px;
  background-color: #000000;
  margin: 30px 0;
}

#main-image {
  width: 100%;
  height: 300px;
  background-size: cover;
  background-position: top;
}

/* button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
} */

#next_ca {
  /* background-color: white; */
  font-size: 50px;
  position: absolute;
  height: 100px;
  justify-content: center;
  align-items: center;
  color: rgb(0, 0, 0);
  z-index: 3;
}

#prev_ca {
  font-size: 50px;
  position: absolute;
  height: 100px;
  justify-content: center;
  align-items: center;
  z-index: 3;
  color: rgb(0, 0, 0);
}

#prev_ca ,#next_ca:hover{
  background-color: rgb(114, 170, 187);
  opacity: 0.8;
}

</style>