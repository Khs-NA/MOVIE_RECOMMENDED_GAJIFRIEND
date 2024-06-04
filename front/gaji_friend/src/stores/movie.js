import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'


export const useCounterStore = defineStore('counter', () => {
  const newMovies = ref([])
  const Movies = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  const getNewMovies = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/new/`
    })
      .then((response) => {
        newMovies.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }

  const getMovies = function() {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/`
    })
      .then((response) => {
        Movies.value = response.data
      })
      .catch((error) => {
        console.log(error)
      })
  }
  
  return { 
    Movies, newMovies, API_URL,
    getNewMovies, getMovies
   }
}, { persist: true })
