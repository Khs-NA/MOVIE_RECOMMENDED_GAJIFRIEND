<template>
  <div id="main-container">
    <div id="signup-box">
      <div id="title">
        <h1>로그인</h1>
        <form @submit.prevent="logIn">
          <div>
            <label for="username">username:</label>
            <input type="text" v-model.trim="username" id="username" />
          </div>
          <div>
            <label for="password">password:</label>
            <input type="password" v-model.trim="password" id="password" />
          </div>
          <div id="loginbutton">
            <input type="submit" />
            <button @click="close">Close</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits  } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from 'vue-router';
const router = useRouter();


const username = ref('');
const password = ref('');
const store = useAuthStore();
const emit = defineEmits(["close"]);

const close = () => {
  emit("close");
};

const logIn = async () => {
  const payload = {
    username: username.value,
    password: password.value,
  };
  await store.logIn(payload);
  closeModal(); // Consider closing only on successful login
};

</script>

<style scoped>
/* #main-container {
  border-radius: 20px;
  background-color: #bfb6ae;
  width: 500px;
  height: 275px;
  margin-top: 200px;
  margin-left: 700px;
  box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15), 0 2px 2px rgba(0, 0, 0, 0.15),
    0 4px 4px rgba(0, 0, 0, 0.15), 0 8px 8px rgba(0, 0, 0, 0.15);
} */
#main-container {
  margin-left: calc(50% - 250px);
  border-radius: 10px;
  background-color: #ffffff;
  opacity: 0.9;
  width: 400px;
  height: 300px;
  padding: 30px;
  margin: 100px auto;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}

#signup-box {
  width: 100%;
}

#title h1 {
  font-size: 24px;
  color: #333333;
  text-align: center;
  margin-bottom: 20px;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

form div {
  margin-bottom: 5px;
  width: 100%;
}

form label {
  display: block;
  font-size: 14px;
  color: #333333;
  margin-bottom: 5px;
}

form input[type="text"],
form input[type="password"] {
  width: calc(100% - 20px);
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 5px;
}

form input[type="submit"],
form button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

form input[type="submit"] {
  background-color: #3498db;
  color: white;
}

form input[type="submit"]:hover {
  background-color: #2980b9;
}

form button {
  background-color: #e74c3c;
  color: white;
  margin-top: 10px; /* Add margin-top to create space between buttons */
}

form button:hover {
  background-color: #c0392b;
}

#loginbutton {
  padding: 30px;
}
</style>
