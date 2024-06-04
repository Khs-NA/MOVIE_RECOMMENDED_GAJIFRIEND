<template>
  <div id="wrap">
    <div id="text">
      <p :class="{ textVisible2: isTextVisible2 }">
        새로운 영화와 새로운 친구를 만나보세요!
      </p>
      <p :class="{ textVisible: isTextVisible, moveUp: isTextMovedUp }">
        Let's make movie mate
      </p>
      <div v-if="isTextVisible2" id="friend-link">
        <RouterLink :to="{ name: 'friend' }">
          <i class="fas fa-user-friends"></i> 친구찾기
        </RouterLink>
      </div>
      <div v-if="isTextVisible2" id="friend-link">
        <RouterLink :to="{ name: 'newMovie' }">
          <i class="fas fa-user-friends"></i> 영화찾기
        </RouterLink>
      </div>
    </div>
    <!-- <div id="visual"></div> -->
    <div id="black"></div>
  </div>
  <div id="pink-box"></div>
</template>

<script setup>

!function(w, d, s, ...args){
  var div = d.createElement('div');
  div.id = 'aichatbot';
  d.body.appendChild(div);
  w.chatbotConfig = args;
  var f = d.getElementsByTagName(s)[0],
  j = d.createElement(s);
  j.defer = true;
  j.type = 'module';
  j.src = 'https://aichatbot.sendbird.com/index.js';
  f.parentNode.insertBefore(j, f);
}(window, document, 'script', '13992300-A2CD-419B-BD67-23C1F36E2BE4', 'onboarding_bot', {
  apiHost: 'https://api-cf-ap-2.sendbird.com',
});
import { RouterLink, RouterView, useRoute, useRouter } from "vue-router";
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { onMounted } from "vue";

const store = useAuthStore();
onMounted(() => {
  store.userDetail();
});
// 유저 추천영화로 가기위해서 이름 받아오기
const route = useRoute();
const router = useRouter();
const detailuser = store.userdetail;

// 추천영화로 이동
const updateRoute = () => {
  console.log("유저확인");
  const username = detailuser.username;
  console.log(username);
  router.push({ name: "movie_name", params: { name: username } });
};

// 마이페이지 이동
const updateRoute2 = () => {
  console.log("유저확인");
  const username = detailuser.username;
  console.log(username);
  router.push({ name: "profile", params: { name: username } });
};

// 로그인 확인
const isAuthenticated = computed(() => {
  return store.isLogin;
});

const isHeader = ref(false);

const changeNav = () => {
  isHeader.value = true;
};

const originNav = () => {
  isHeader.value = false;
};

// useAuthStore에서 logOut 함수를 추출합니다.
const { logOut } = useAuthStore();

const isSign = ref(false);
const isLogin = ref(false);

const sighUp = function () {
  isSign.value = true;
};

const logIn = function () {
  isLogin.value = true;
};

const isTextVisible = ref(false);
const isTextVisible2 = ref(false);
const isTextMovedUp = ref(false);
// 화면 효과
onMounted(() => {
  const blackElement = document.getElementById("black");
  setTimeout(() => {
    blackElement.classList.add("BlackActive");
  }, 250);
  setTimeout(() => {
    isTextVisible.value = true;
  }, 2000);
  setTimeout(() => {
    isTextMovedUp.value = true;
  }, 3000);
  setTimeout(() => {
    isTextVisible2.value = true;
  }, 4700); // slight delay to ensure the first text has moved up
});
</script>

<style scoped>
#header {
  height: 64px;
  width: 100%;
  position: absolute;
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: 800px;
  font-style: bold;
  z-index: 100;
}

#header p {
  position: absolute;
  left: 10px;
  top: 20px;
}

#header .nav {
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  top: 20px;
  width: 100%;
}

#header .nav .link1,
#header .nav .link2 {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 5px 0;
}

#header .nav .link2 {
  margin-top: -30px;
  margin-left: 1500px;
}

#header .nav .link1 * {
  margin: 5px 12px;
  text-decoration: none;
}

#header .nav .link2 * {
  margin: 0 4px;
}

#text {
  color: rgba(255, 255, 255, 0);
  position: absolute;
  top: 300px;
  left: 200px;
  font-family: "Noto Sans KR", sans-serif;
  font-optical-sizing: auto;
  font-weight: 900px;
  font-size: 100px;
  font-style: bold;
  z-index: 1;
}

.textVisible {
  color: white;
  animation: fadeIn 3s ease-in-out forwards; /* 텍스트가 나타나는 애니메이션 */
}

.moveUp {
  animation: moveUp 1s ease-in-out forwards; /* 텍스트가 살짝 위로 이동하는 애니메이션 */
}

.textVisible2 {
  bottom: 200px;
  color: white;
  animation: fadeIn 1s ease-in-out forwards; /* 두 번째 텍스트가 나타나는 애니메이션 */
  font-size: 50px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeIn2 {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

#friend-link {
  margin-top: -100px;
  font-size: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: fadeIn3 1s ease-in-out forwards;
}

#friend-link a {
  color: white;
  text-decoration: none;
}

#friend-link i {
  font-size: 30px;
}

@keyframes fadeIn3 {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes moveUp {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-300px);
  }
}

#visual {
  height: 990px;
  background: url(/public/bgi.png) no-repeat center center;
  background-size: cover;
  z-index: 1;
}

#black {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition-duration: 2.5s;
  z-index: 0;
}

.BlackActive {
  background-color: rgba(0, 0, 0, 0.796);
}

@media (max-width: 1200px) {
  #header .nav {
    justify-content: flex-start;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
  }
}

@media (max-width: 768px) {
  #header {
    height: auto;
  }
  #header p {
    position: static;
    margin: 10px 0;
    text-align: center;
  }
  #header .nav {
    position: static;
    flex-direction: column;
    align-items: center;
  }
  #header .nav .link1,
  #header .nav .link2 {
    justify-content: center;
    margin: 5px 0;
  }
  #header .nav .link2 {
    position: static;
    flex-direction: column;
    align-items: center;
  }
  #visual {
    height: 700px;
  }
}

@media (max-width: 480px) {
  #header .nav .link1 * {
    margin: 5px 10px;
    font-size: 14px;
  }
  #header .nav .link2 {
    font-size: 14px;
  }
  #visual {
    height: 700px;
  }
}
</style>
