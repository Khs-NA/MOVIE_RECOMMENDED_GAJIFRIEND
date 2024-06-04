<template>
  <div>
    <div id="blackContainer"></div>
      <h1>📖게시글 상세 정보</h1>
      <div id="post-container">
     <div id="post-title">
        <p>{{ store.detailPost.title }}</p>
      </div>
      <div id="post-info">
        <span class="post-id">No.{{ store.detailPost.id }}</span>
        <span>작성자 : {{ store.detailPost.create_user }}</span>
      </div>
      <div id="post-dates">
        <span class="created-date">작성일: {{ store.detailPost.created_at?.slice(0,10) }}</span>
        <span> | </span>
        <span class="updated-date">수정일: {{ store.detailPost.updated_at?.slice(0,10) }}</span>
      </div>
      <div id="post-content">
        <p class="post-content">{{ store.detailPost.content }}</p>
      </div>
      <div id="action-buttons">
        <button @click="editPost(store.detailPost.id)" class="edit-button">수정</button>
        <button @click="deletePost(store.detailPost.id)" class="delete-button">삭제</button>
      </div>
      <div id="comments">
        <CommentCreate :postPk="store.detailPost.id"/>
        <div>
          <ul>
            <CommentList
              v-for="comment in store.detailPost.comment_set"
              :key="comment.id"
              class="comment-item"
              :comment="comment"
            />
          </ul>
        </div>
    </div> 
  </div>
  </div>
</template>

<script setup>
import CommentCreate from '../components/CommentCreate.vue';
import CommentList from '../components/CommentList.vue';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { usePostStore } from '../stores/posts';


const route = useRoute();
const router = useRouter();
const store = usePostStore();

onMounted(() => {
  store.getDetailPost(route.params.id)
});

const deletePost = async (id) => {
  if (confirm('정말로 삭제하시겠습니까?')) {
    await store.deletePost(id);
    router.push({ name: 'ArticleView' }); // Redirect after delete
  }
}

const editPost = (id) => {
  router.push({ name: 'UpdateView', params: { id: id } }); // Navigate to the edit page
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

#post-container {
  position: absolute;
  top: 230px;
  left: 570px;
  width: 800px;
  height: 600px;
  background-color: rgba(184, 184, 184, 0.751);
  border: 1px solid #000000;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  position: absolute;
  top: 120px;
  left: 800px;
  font-size: 2rem;
  color: #ffffff;
}


/* Additional styling for buttons */
.delete-button, .edit-button {
  margin: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
}

.delete-button {
  background-color: #ff4d4f;
  color: white;
}

.edit-button {
  background-color: #4caf50;
  color: white;
}

.delete-button:hover, .edit-button:hover {
  opacity: 0.8;
}

#post-content > p {
  margin-bottom: 0;
}


#post-title, #post-info, #post-content, #post-dates, #comments {
  border: 1px solid black;
  background-color: white;
  width: 100%;
  padding: 10px;
  display: flex;
  align-items: center;
}

#post-title {
  height: 60px;
}

#post-title > p {
  font-weight: bold;
  margin-bottom: 0;
}

#post-info {
  justify-content: space-between;
}

#post-dates {
  justify-content: right;
}

#post-content {
  height: 260px;
}

#post-content > p {
  position: relative;
  top: -100px;
}

#comments {
  height: 90px;
}
</style>
