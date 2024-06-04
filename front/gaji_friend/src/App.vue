<template>
  <div>
    <header id="header">
      <div id="logoicon">
        <img src="/logo.png" alt="" id="logo" />
        <p class="inner">가지친구</p>
      </div>
      <nav class="nav">
        <ul class="link1">
          <RouterLink :to="{ name: 'main' }" id="perLink">HOME</RouterLink>
          <RouterLink :to="{ name: 'newMovie' }" id="perLink">최신영화</RouterLink>
          <a @click="updateRoute" id="recMovie">추천 영화</a>
          <RouterLink :to="{ name: 'friend' }" id="perLink">친구찾기</RouterLink>
          <RouterLink :to="{ name: 'ArticleView' }" id="perLink">커뮤니티</RouterLink>
        </ul>
        <ul class="link2">
          <span v-if="isAuthenticated">
            <a @click="updateRoute2">마이 페이지</a>
          </span>
          <span> | </span>
          <RouterLink :to="{ name: 'signup' }" id="perLink">회원가입</RouterLink>
          <span> | </span>

          <span v-if="!isAuthenticated" id="loginwindow">
            <a @click="openModal" id="login_a">로그인</a>
            <LogInModal v-if="showModal" @close="closeModal" />
          </span>
          <span v-else>
            <button @click="logOut" id="logout">로그아웃</button>
          </span>
        </ul>
      </nav>
    </header>
    <RouterView />
    <div id="visual"></div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from "vue-router";
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { onMounted } from "vue";
import LogInModal from "./components/LogInModal.vue";

const store = useAuthStore();
onMounted(() => {
  store.userDetail();
});
const route = useRoute();
const router = useRouter();
const detailuser = store.userdetail;

const updateRoute = () => {
  const username = detailuser.username;
  router.push({ name: "movie_name", params: { name: username } });
};

const updateRoute2 = () => {
  const username = detailuser.username;
  router.push({ name: "profile", params: { name: username } });
};

const isAuthenticated = computed(() => {
  return store.isLogin;
});

const { logOut } = useAuthStore();

const showModal = ref(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};
</script>

<style scoped>
#header {
  height: 64px;
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
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
  color: white;
}

#header .nav {
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  top: 20px;
  width: 100%;
  text-decoration: none;
}

#header .nav .link1 {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 5px 0;
  color: white;
}

#header .nav .link2 {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 5px 0;
  color: white;
}

#header .nav .link2 {
  margin-top: -30px;
  margin-left: 1500px;
}

#header .nav .link1 * {
  margin: 5px 12px;
  text-decoration: none;
}

#recMovie {
  color: #e3fef7;
}

#header .nav .link2 * {
  margin: 0 4px;
  text-decoration: none;
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
}

@media (max-width: 480px) {
  #header .nav .link1 * {
    margin: 5px 10px;
    font-size: 14px;
  }

  #header .nav .link2 {
    font-size: 14px;
  }
}

#visual {
  height: 100vh;
  background: url(/public/bgi.png) no-repeat center center;
  background-size: cover;
  z-index: -1;
}

#logout {
  font-size: 1em;
  padding: 10px 20px;
  color: white;
  background-color: #e74c3c;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

#logout:hover {
  background-color: #c0392b;
}

#loginwindow {
  background-color: rgb(49, 22, 169);
  bottom: 300px;
}

#login_a:hover {
  background-color: #9287ba;
}

#logoicon {
  width: 30px;
  height: 30px;
  margin-left: 30px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

#logo {
  width: 35px;
  margin-left: 10px;
}

.inner {
  margin-left: 60px;
  margin-top: 10px;
  font-size: 15px;
  color: white;
  display: flex;
}
</style>
