<template>
  <div>
    <div id="blackContainer"></div>
    <div id="genre-container">
      <label for="genre"> 
      <select v-model="selectedGenre" id="genre">
        <option v-for="(genreName, genreId) in genreMapping" :key="genreId" :value="genreName">
          {{ genreName }}
        </option>
      </select>
      <span id="genreintro"> 장르를 좋아하는 친구들 입니다.</span>
      </label>
    </div>
    <div id="friend">
      <div v-for="(chunk, index) in friendChunks" :key="index" class="friend-row">
          <FriendSearchMovie v-for="friend in chunk" :key="friend.pk" :friend="friend" />
      </div>
    </div>
  </div>
</template>

<script setup>
import FriendSearchMovie from '@/components/FriendSearchMovie.vue';
import { useCommunityStore } from '@/stores/community';
import { ref, watch, computed } from 'vue';

const store = useCommunityStore();
const userList = computed(() => store.users);
const friendList = ref([]);

// 장르 목록
const genreMapping = {
  1: "모험",
  2: "판타지",
  3: "애니메이션",
  4: "드라마",
  5: "공포",
  6: "액션",
  7: "코미디",
  8: "역사",
  9: "서부",
  10: "스릴러",
  11: "범죄",
  12: "다큐멘터리",
  13: "SF",
  14: "미스터리",
  15: "음악",
  16: "로맨스",
  17: "가족",
  18: "전쟁",
  19: "TV 영화"
};
const selectedGenre = ref(Object.values(genreMapping)[0]); // 기본값 설정

// 선택된 장르에 맞는 친구 목록을 업데이트하는 함수
const updateFriendList = () => {
  friendList.value = userList.value.filter(user => user.genre === selectedGenre.value);
};

// 선택된 장르가 변경될 때마다 friendList를 업데이트
watch(selectedGenre, updateFriendList, { immediate: true });

// 친구 목록을 두 개씩 묶는 함수
const chunkArray = (array, chunkSize) => {
  const chunks = [];
  for (let i = 0; i < array.length; i += chunkSize) {
    chunks.push(array.slice(i, i + chunkSize));
  }
  return chunks;
};

// 친구 목록을 두 개씩 묶은 데이터
const friendChunks = computed(() => chunkArray(friendList.value, 2));

const friend = () => {

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

#genre-container {
  position: absolute;
  top: 120px;
  left: 100px;
  color: white;
  font-size: 24px;
  text-shadow: 2px 3px 10px #7E8C95;
}

#friend {
  position: absolute;
  height: 630px;
  width: 1770px;
  top: 200px;
  left: 10px;
  overflow-y: auto;
}

#friend::-webkit-scrollbar {
  width: 5px;
}

#friend::-webkit-scrollbar-thumb {
  height: 0.5px;
  background: #F2D8D5;
  border-radius: 10px;
}

#friend::-webkit-scrollbar-track {
  background-color: #BFB6AE;
}
/* 필요한 스타일을 여기에 추가하세요 */
.friend-row {
  display: flex;
  justify-content: space-between;
}

/* 
label {
  font-size: 16px;
  color: #333;
  margin-bottom: 10px;
}

select {
  margin-top: 10px;
  margin-left: 20px;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #ff69b4;
  border-radius: 8px;
  background-color: #fff;
  color: #333;
  transition: border-color 0.3s, box-shadow 0.3s;
}

select:focus {
  border-color: #ff85c0;
  outline: none;
  box-shadow: 0 0 10px rgba(255, 105, 180, 0.3);
}
option {
  background-color: #fff;
  color: #333;
  padding: 10px;
  font-size: 16px;
  font-family: 'Arial', sans-serif;
} */

/* Option styling */
/* select option {
  padding: 10px;
  font-size: 16px;
  color: #000000; 
  background-color: #fdfdfd; 
  border-bottom: 1px solid #ff69b4; 
}
#genreintro {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-top: 10px;
  margin-left: 5px;
  padding: 8px 12px;
  background-color: #f8f8f8;
  border-radius: 8px;
  border: 1px solid #ddd;
  display: inline-block;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
} */
</style>
