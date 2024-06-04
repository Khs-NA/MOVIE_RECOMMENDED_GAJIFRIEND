import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'


export const usePostStore = defineStore('post', () => {
  const postList = ref([])
  const detailPost = ref([])
  const authStore = useAuthStore()
  const token = ref(authStore.token)

  const getPostList = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/api/v1/articles/',
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      postList.value = response.data  
    } catch (error) {
      console.error('Failed to fetch post list:', error)
    }
  }

  const getDetailPost = async (pk) => {
    try {
      const response = await axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/articles/${pk}`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      detailPost.value = response.data
    } catch (error) {
      console.error('Failed to fetch post detail:', error)
    }
  }

  const createPost = async ({ title, content }) => {
    try {
      await axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/v1/articles/',
        data: {
          title,
          content
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
    } catch (error) {
      console.error('Failed to create post:', error)
    }
  }


  const deletePost = async (id) => {
    axios({
      method: 'delete', // Using 'put' method for updating
      url: `http://127.0.0.1:8000/api/v1/articles/${id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      console.log('삭제 성공', response.data);
    })
    .catch(error => {
      console.error('Failed to update post:', error);
    });
  };



  return { postList, getPostList, detailPost, getDetailPost, createPost, deletePost}
},{ persist: true })