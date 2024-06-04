<template>
  <div>
    <h1>친구가 좋아요한 영화입니다</h1>
    <!-- 좋아요 수 만큼 반복 -->
    <div id="container" v-for="n in 4">
      <!-- 이미지 주소 바꾸기 -->
      <img src="https://image.tmdb.org/t/p/w300//qV9BQZdiM8foEzDz0Ag5hGWE5qM.jpg" alt="">
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
#container {
  display: inline-block;
  margin: 0 15px;
}
</style>