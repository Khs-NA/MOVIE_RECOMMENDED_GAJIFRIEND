import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'
import { useRouter } from 'vue-router'

export const useCommunityStore = defineStore('community', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const authStore = useAuthStore()
  const token = authStore.token
  const articles = ref([])
  const router = useRouter()
  const users = ref([])
  const followings = ref([]);

  const getArticlse = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then(response => {
      articles.value = response.data
    })
    .catch(error => {
      console.log(error)
    })
  }
  
  const getusers = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/user/userlist/`
    })
      .then((response) => {
        users.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
  

  // const getFollowings = () => {
  //   axios({
  //     method: 'get',
  //     url: `${API_URL}/api/v1/friend/followings/`,
  //     headers: {
  //       'Authorization': `Token ${token.value}`
  //     }
  //   })
  //   .then(response => {
  //     followings.value = response.data;
  //   })
  //   .catch(error => {
  //     console.error('팔로잉 리스트를 가져오는 중 오류가 발생했습니다.', error);
  //   });
  // }

  return { 
    articles, API_URL, users,
    getArticlse, getusers, 
   }
}, { persist: true })
