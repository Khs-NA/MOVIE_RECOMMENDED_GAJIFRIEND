<template>
  <div id="main-container">
      <div id="signup-box">
        <div id="title">
        <h1>로그인</h1>
        <form @submit.prevent="logIn">
          <div>
            <label for="username">username : </label>
            <input type="text" v-model.trim="username" id="username">
          </div>
          <div>
            <label for="password">password : </label>
            <input type="password" v-model.trim="password" id="password">
          </div>
          <input type="submit">
        </form>
      </div>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  
  const username = ref(null)
  const password = ref(null)
  const store = useAuthStore()
  
  const logIn = function () {
    const payload = {
      username: username.value,
      password: password.value
    }
    store.logIn(payload)
  }
  
  </script>
  
  <style scoped>

  #main-container {
    border-radius: 20px;
    background-color: #BFB6AE;
    width: 500px;
    height: 275px;
    margin-top: 200px;
    margin-left: 700px;
    box-shadow: 0 1px 1px rgba(0,0,0,0.15), 
              0 2px 2px rgba(0,0,0,0.15), 
              0 4px 4px rgba(0,0,0,0.15), 
              0 8px 8px rgba(0,0,0,0.15);
  }
  /* html, body {
      height: 100%;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #f0f0f0;
  }
  
  
  #signup-box {
      width: 50%;
      max-width: 600px;
      padding: 20px;
      background-color: white;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      border-radius: 8px;
  }
  
  #title {
      text-align: center;
      margin-bottom: 20px;
  }
  
  form {
      display: flex;
      flex-direction: column;
  }
  
  form div {
      margin-bottom: 15px;
  }
  
  form label {
      margin-bottom: 5px;
      font-weight: bold;
  }
  
  form input[type="text"],
  form input[type="password"],
  form input[type="submit"] {
      width: 100%;
      padding: 10;
      width: 100%;
      padding: 10px;
      font-size: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
  }
  
  form input[type="submit"] {
      padding: 10px;
      font-size: 18px;
      background-color: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      margin-top: 20px;
  }
  
  form input[type="submit"]:hover {
      background-color: #0056b3;
  } */
  </style>
  