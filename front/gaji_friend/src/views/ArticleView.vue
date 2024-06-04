<template>
  <div>
    <div id="blackContainer"></div>
    <div id="box">
      <h1>게시글 목록 페이지</h1>
      <RouterLink :to="{ name: 'CreateView' }" id="create"> 게시글 생성</RouterLink>
      <ul id="list">
        <div class="post-container" v-for="post in paginatedPosts" :key="post.id" :post="post" @click="goDetail(post.id)">
          <p>No.{{ post.id }}</p>
          <hr>
          <p>작성자 : {{ post.create_user}}</p>
          <p>제목 : {{ post.title }}</p>
        </div>
      </ul>
    </div>
    <div class="pagination">
      <button @click="prevPage">❮</button>
      <button @click="nextPage">❯</button>
    </div>
        <div class="pagination">
        <button @click="prevPage">❮</button>
        <button @click="nextPage">❯</button>
      </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref, computed } from 'vue';
import { usePostStore } from '../stores/posts';
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const store = usePostStore()
const route = useRoute()

const currentPage = ref(1)
const pageSize = 8

const totalPages = computed(() => {
  return Math.ceil(store.postList.length / pageSize)
})

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return store.postList.slice(start, end)
})

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

onMounted(() => {
  store.getPostList()

})


const goDetail = (id) => {
  router.push({ name: 'DetailView', params: { id: id } })
}

</script>

<style scoped>
#blackContainer {
  position: fixed;
  width: 2000px;
  height: 1000px;
  background-color: #000000c7;
  z-index: 0;
}

#box {
  position: absolute;
  border: 2px solid black;
  border-radius: 20px;
  background-color: rgb(19, 93, 102, 0.5);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); 
  width: 1000px;
  height: 600px;
  top: 210px;
  left: 480px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
 
}

h1 {
  color: white;
}

#create {
  border: 2px solid black;
  border-radius: 5px;
  width: 130px;
  text-align: center;
  text-decoration: none;
  margin-top: 10px ;
  color: #000000;
  background-color: rgb(216, 223, 222);
  font-weight: bold;
}

#list {
  list-style-type: none;
  padding-top: 30px;
  padding-left: 60px;
}

.post-container {
  display: inline-block;
  text-align: center;
  padding: 30px;
  border-radius: 20px;
  border: 2px solid black;
  background-color: rgb(227, 254, 247) ;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  width: 200px;
  height: 180px;
  margin: 15px 10px;
  overflow: hidden;
}

.pagination {
  position: absolute;
  /* display: flex;
  justify-content: center;
  align-items: center; */
  top: 850px;
  left: 925px;
}

.pagination>* {
  margin: 10px;
}
</style>