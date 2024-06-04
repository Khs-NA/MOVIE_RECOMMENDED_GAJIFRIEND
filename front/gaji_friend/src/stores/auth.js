import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const userdetail = ref([])
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  const signUp = function (payload) {
    // 1. 사용자 입력 데이터를 받아
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password2, nickname, age, genre, gender, location ,longitude_x, latitude_y } = payload
    console.log(genre)
    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        // username: username,
        // password1: password1,
        // password2: password2
        username, password1, password2, nickname, age, genre, gender, location, longitude_x, latitude_y
      }
    })
     .then((response) => {
       console.log('회원가입 성공!')
       const password = password1
       logIn({ username, password })
     })
     .catch((error) => {
       console.log(error)
       console.log('회원가입 실패')
     })
  }



  const logIn = function (payload) {
    // 1. 사용자 입력 데이터를 받아
    const { username, password } = payload
    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((response) => {
        console.log('로그인 성공!')
        console.log(response.config.data)
        // console.log(response.data.key)
        // 3. 로그인 성공 후 응답 받은 토큰을 저장
        token.value = response.data.key
        // username.value = response.data.username
        router.push({ name : 'main' })
      })
      .catch((error) => {
        console.log(error)
      })
  }




  // 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
          'Authorization': `Token ${token.value}`  // token.value를 사용하여 헤더에 토큰을 동적으로 추가
      }
  })
  .then(response => {
      console.log('Logged out successfully:', response.data);
      token.value = null
      // 로그아웃 성공 후 추가적인 로직 수행, 예를 들어 메인 페이지로 리다이렉트
      router.push('/')
  })
  .catch(error => {
      console.error('Logout failed:', error);
      // 로그아웃 실패 처리 로직
  });
  }


  // 유저 정보 받기
  const userDetail = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/`,
      headers: {
          'Authorization': `Token ${token.value}`  // token.value를 사용하여 헤더에 토큰을 동적으로 추가
      }
  })
  .then(response => {
      console.log('유저 정보 불러오기 성공');
      console.log(response.data)
      userdetail.value = response.data
      // 로그아웃 성공 후 추가적인 로직 수행, 예를 들어 메인 페이지로 리다이렉트
      
  })
  .catch(error => {
      console.error('유저 정보 불러오기 실패', error);
      // 로그아웃 실패 처리 로직
  });
  }

  return { 
    API_URL, token,  isLogin, userdetail,
   signUp, logIn, logOut,userDetail
   }
}, { persist: true })
