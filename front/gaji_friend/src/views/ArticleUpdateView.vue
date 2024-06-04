<template>
  <div id="blackContainer"></div>
  <div class="edit-post-page">
    <h1 style="font-size: 30px; font-weight: bold;">게시글 수정</h1>
    <form @submit.prevent="updatePost(post.id)" class="post-form">
      <label for="title" class="form-label">제목:</label>
      <input type="text" id="title" v-model="post.title" class="form-input" required>

      <label for="content" class="form-label">내용:</label>
      <textarea id="content" cols="30" rows="10" v-model="post.content" class="form-textarea" required></textarea>

      <button type="submit" class="submit-button">게시글 수정</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePostStore } from '@/stores/posts';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';


const route = useRoute();
const router = useRouter();
const store = usePostStore();
const authstore = useAuthStore()
const post = ref({ title: '', content: '' });
const token = ref(null)


onMounted(async () => {
  await store.getDetailPost(route.params.id);
  post.value = { ...store.detailPost };
  token.value = authstore.token
});

const updatePost = async (pk) => {
  axios({
    method: 'put', // Using 'put' method for updating
    url: `http://127.0.0.1:8000/api/v1/articles/${pk}/`,
    data: {
      title: post.value.title,
      content: post.value.content
    },
    headers: {
      Authorization: `Token ${token.value}`
    }
  })
  .then(response => {
    console.log('업데이트 성공', response.data);
    router.push({ name: 'DetailView', params: { id: pk } }); // Redirect after success
  })
  .catch(error => {
    console.error('Failed to update post:', error);
  });
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

.edit-post-page {
  position: absolute;
  bottom: 200px;
  left: 650px;
  width: 700px;
  margin: 0 auto;
  padding: 20px;
  background-color: rgba(184, 184, 184, 0.7);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
}

.post-form {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  color: #555;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 10px;
  z-index: 1;
}

.form-input:focus, .form-textarea:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.submit-button {
  display: block;
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background: linear-gradient(-45deg, #8e44ad 0%, #c0392b 100%);
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
  z-index: 1;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>