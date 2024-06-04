<template>
  <div class="movie-detail">
    <img :src="image_url + newMovie.poster_path" :alt="newMovie.poster_path" />
  </div>
</template>

<script setup>
import { defineProps, ref } from "vue";

defineProps({
  newMovie: Object,
});

const image_url = "https://image.tmdb.org/t/p/w300/";
</script>
<style scoped>
#movie-detail {
  position: relative;
  widows: 400px;
  height: 450px;
  z-index: 2000;
}
</style>
