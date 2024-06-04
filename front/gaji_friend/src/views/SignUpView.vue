<template>
  <div id="main-container">
    <div id="blackContainer">
      <div id="signup-box">
        <div id="title">
          <h2>회원가입</h2>
        </div>

        <div id="content">
          <form @submit.prevent="signUp">
            <div>
              <label for="username">username : </label>
              <input type="text" v-model.trim="username" id="username" />
            </div>
            <div>
              <label for="password1">password : </label>
              <input type="password" v-model.trim="password1" id="password1" />
            </div>
            <div>
              <label for="password2">password 확인: </label>
              <input type="password" v-model.trim="password2" id="password2" />
            </div>
            <div>
              <label for="nickname">nickname : </label>
              <input type="text" v-model.trim="nickname" id="nickname" />
            </div>
            <div>
              <label for="age">age : </label>
              <input
                type="number"
                min="1"
                max="120"
                v-model.trim="age"
                id="age"
              />
            </div>
            <div id="detail">
              <div id="info">
                <div id="genre">
                  <label for="genre">genre : </label>
                  <select v-model="genre">
                    <option
                      v-for="(genreName, genreId) in genreMapping"
                      :key="genreId"
                      :value="genreName"
                    >
                      {{ genreName }}
                    </option>
                  </select>
                </div>
                <div id="gender">
                  <label for="gender">gender : </label>
                  <select v-model="gender">
                    <option
                      v-for="(genderName, genderId) in genderMapping"
                      :key="genderId"
                      :value="genderName"
                    >
                      {{ genderName }}
                    </option>
                  </select>
                </div>
              </div>
              <div id="location">
                <div id="do">
                  <label for="do">도 : </label>
                  <select v-model="selectedDo">
                    <option
                      v-for="(loc, index) in uniqueDos"
                      :key="index"
                      :value="loc"
                    >
                      {{ loc }}
                    </option>
                  </select>
                </div>
                <div id="city">
                  <label for="city">시/군/구 : </label>
                  <select v-model="selectedCity" :disabled="!selectedDo">
                    <option
                      v-for="(loc, index) in filteredCities"
                      :key="index"
                      :value="loc.city"
                    >
                      {{ loc.city }}
                    </option>
                  </select>
                </div>
              </div>
            </div>
            <input type="submit" value="Signup" />
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useAuthStore } from "@/stores/auth";
// import locData from '.../GaJi_Movie_And_Friend_Recommended/back/asset/loc.json'

import locData from "@/assets/loc.json";

// 장르 매핑 딕셔너리
const genreMapping = {
  12: "모험",
  14: "판타지",
  16: "애니메이션",
  18: "드라마",
  27: "공포",
  28: "액션",
  35: "코미디",
  36: "역사",
  37: "서부",
  53: "스릴러",
  80: "범죄",
  99: "다큐멘터리",
  878: "SF",
  9648: "미스터리",
  10402: "음악",
  10749: "로맨스",
  10751: "가족",
  10752: "전쟁",
  10770: "TV 영화",
};

// 성별 매핑 딕셔너리
const genderMapping = {
  M: "남성",
  F: "여성",
};

const username = ref(null);
const password1 = ref(null);
const password2 = ref(null);
const nickname = ref(null);
const age = ref(null);
const genre = ref(null);
const gender = ref(null);
const selectedDo = ref(null);
const selectedCity = ref(null);
// const profileImage = ref(null)
const store = useAuthStore();

const uniqueDos = computed(() => {
  const dos = locData.map((loc) => loc.do);
  return [...new Set(dos)];
});

const filteredCities = computed(() => {
  return locData.filter((loc) => loc.do === selectedDo.value);
});

const signUp = function () {
  const selectedLoc = locData.find(
    (loc) => loc.do === selectedDo.value && loc.city === selectedCity.value
  );
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    age: age.value,
    genre: genre.value,
    gender: gender.value,
    location: `${selectedDo.value} ${selectedCity.value}`,
    longitude_x: selectedLoc ? selectedLoc.longitude : null,
    latitude_y: selectedLoc ? selectedLoc.latitude : null,
  };
  store.signUp(payload);
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

#signup-box {
  position: absolute;
  width: 490px;
  height: 840px;
  padding: 20px;
  background-color: white;
  top: 110px;
  left: 700px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.813);
  border-radius: 8px;
  opacity: 0.8;
}

#content {
  display: flex;
  flex-direction: column;
}

form {
  display: flex;
  flex-direction: column;
}

form div {
  margin-bottom: 15px;
}

form label {
  margin-bottom: 5px;
  font-weight: bold;
}

form input[type="text"],
form input[type="password"],
form input[type="number"],
form select {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

form input[type="submit"] {
  padding: 10px;
  font-size: 18px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;
}

form input[type="submit"]:hover {
  background-color: #0056b3;
}

#info,
#location {
  width: 300px;
  display: flex;
  flex-direction: row;
}

#do,
#city,
#genre,
#gender {
  width: 130px;
  margin: 0 10px;
}

/* #main-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 50px;
  }
  
  #signup-box {
    border-radius: 70px;
    width: 1100px;
    height: 600px;
    background-color: #fff;
  }
  
  #title {
    position: relative;
    left: 100px;
  }
  
  #content {
    position: relative;
    left: 300px;
    top: 100px;
  } */
</style>
