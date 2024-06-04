<template>
  <div>
    <h1>{{ friend.name }}님의 상세 페이지</h1>
    <div id="container">
      <div id="main-info">
        <div id="image">프사</div>
        <div id="sub-info">
          <div id="nickname">닉네임</div>
          <div id="age">나이</div>
          <div id="gender">성별</div>
          <div id="location">지역</div>
        </div>
      </div>
      <div id="add-friend"></div>
      <div id="one-liner"></div>
      <div id="liked-genre"></div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'




const route = useRoute()
const name = route.params.name
</script>

<style scoped>
#container {
  border: 1px solid black;
  width: 400px;
  height: 570px;
}

#main-info {
  display: flex;
  border: 1px solid black;
  width: 100%;
  height: 45%
}

#image {
  border: 1px solid black;
  width: 45%;
  height: 100%;
}

#sub-info {
  border: 1px solid black;
  width: 55%;
  height: 100%;
}

#nickname {
  border: 1px solid black;
  width: 100%;
  height: 40%;

}
#age, #gender, #location {
  border: 1px solid black;
  width: 100%;
  height: 20%;
}

#add-friend {
  border: 1px solid black;
  width: 100%;
  height: 15%
}

#one-liner {
  border: 1px solid black;
  width: 100%;
  height: 25%
}

#liked-genre {
  border: 1px solid black;
  width: 100%;
  height: 15%
}
</style>