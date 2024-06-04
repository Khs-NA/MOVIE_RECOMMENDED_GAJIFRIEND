import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './auth'
import { usePostStore } from './posts.js'


export const useCommentStore = defineStore('comment', () => {
  const postStore = usePostStore()
  const authStore = useAuthStore()
  const token = ref(authStore.token)
  const commentCreate = async (pk, content) => {
    try {
      const response = await axios({
        method: 'post',
        url: `http://127.0.0.1:8000/api/v1/articles/${pk}/comments/`,
        data: { content },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      // Ensure comment_set is an array
      if (!Array.isArray(postStore.detailPost.comment_set)) {
        postStore.detailPost.comment_set = []
      }
      postStore.detailPost.comment_set.push(response.data)
    } catch (err) {
      console.error('Error creating comment:', err)
    }
  }
  return { commentCreate }
}, { persist: true })