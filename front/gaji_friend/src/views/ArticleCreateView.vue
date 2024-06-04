<template>
  <div>
    <div id="blackContainer"></div>
     <h1>✒게시글 생성 페이지</h1>
    <form @submit.prevent="createPost" class="post-form">
      <label for="title" class="form-label">제목:</label>
      <input type="text" name="title" v-model="title" class="form-input" required>

      <label for="content" class="form-label">내용:</label>
      <textarea name="content" id="content" cols="30" rows="10" v-model="content" class="form-textarea" required></textarea>

      <button class="submit-button">게시글 생성</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { usePostStore } from '@/stores/posts';
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const title = ref('');
const content = ref('');
const postStore = usePostStore();

const createPost = function () {
  const post = {
    title: title.value,
    content: content.value,
  };
  postStore.createPost(post);
  router.push({ name: 'ArticleView' });
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
  top: 120px;
  left: 800px;
  font-size: 2rem;
  color: #ffffff;
}

.post-form {
  position: absolute;
  top: 230px;
  left: 570px;
  width: 800px;
  height: 600px;
  background-color: rgba(150, 150, 150, 0.127);
  border: 1px solid #000000;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-label {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 8px;
  color: #ffffff;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
  transition: border-color 0.2s;
}

.form-textarea {
  height: 390px;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.submit-button {
  display: block;
  width: 100%;
  padding: 12px;
  font-size: 18px;
  background-color: rgb(251, 203, 203);
  color: #070707;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-button:hover {
  background-color: #0056b3;
}

.submit-button:active {
  background-color: #004494;
}

.submit-button:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}
</style>
