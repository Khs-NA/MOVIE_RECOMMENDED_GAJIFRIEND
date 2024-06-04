import { createRouter, createWebHistory } from 'vue-router'
import movieView from '@/views/movieView.vue'
import HomeView from '@/views/homeView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ArticleView from '@/views/ArticleView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import ArticleUpdateView from '@/views/ArticleUpdateView.vue'
import MovieNameView from '@/views/MovieNameView.vue'
import ProfileView from '@/views/ProfileView.vue'
import FriendView from '@/views/FriendView.vue'
import FriendSearchView from '@/views/FriendSearchView.vue'
import FriendNameView from '@/views/FriendNameView.vue'
import FriendListView from '@/views/FriendListView.vue'
import FriendLikeMovieView from '@/views/FriendLikeMovieView.vue'
import TheaterView from '@/views/TheaterView.vue'
import { useAuthStore } from '@/stores/auth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      // 랜딩페이지
      path: '/',
      name: 'main',
      component: HomeView
    },
    {
      // 최신영화
      path: '/movies/new',
      name: 'newMovie',
      component: movieView
    },
    {
      // 추천영화
      path: '/movies/:name',
      name: 'movie_name',
      component : MovieNameView
    },
    {
      // 회원가입
      path: '/signup',
      name: 'signup',
      component: SignUpView,
      beforeEnter: (to, from) => {
        const store = useAuthStore()
        if (store.isAuthenticated) {
          return { name: 'main' }
        }
      }
    },
    {
      // 게시판, 전체 게시글 보기
      path: '/articles',
      name: 'ArticleView',
      component: ArticleView
    },
    {
      // 게시글 보기
      path: '/articles/:id',
      name: 'DetailView',
      component: ArticleDetailView
    },
    {
      // 게시글 생성
      path: '/create',
      name: 'CreateView',
      component: ArticleCreateView
    },
    {
      path: '/update/:id',
      name: 'UpdateView',
      component: ArticleUpdateView

    },
    {
      // 마이페이지
      path: '/user/:name',
      name : 'profile',
      component: ProfileView
    },
    {
      // 친구찾기 메인
      path: '/friend',
      name : 'friend',
      component: FriendView
    },
    {
      // 친구찾기 상세페이지
      path: '/friend/:name',
      name : 'friend_name',
      component: FriendNameView
    },
    {
      // 친구찾기
      path: '/friend/search',
      name : 'friend_search',
      component: FriendSearchView
    },
    {
      // 친구목록
      path: '/friend/list',
      name : 'friend_list',
      component: FriendListView
    },
    {
      // 친구가 좋아요한 영화
      path: '/friend/like_movie',
      name : 'friend_like_movie',
      component: FriendLikeMovieView
    },
    {
      // 영화관
      path: '/friend/theater',
      name : 'theater',
      component: TheaterView
    },

  ]
})

router.beforeEach((to, from) => {
  const store = useAuthStore()
  if (to.name === 'ArticleView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return {name: 'main'}
  }
})


router.beforeEach((to, from) => {
  const store = useAuthStore()
  if (to.name === 'movie_name' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return {name: 'main'}
  }
})

router.beforeEach((to, from) => {
  const store = useAuthStore()
  if (to.name === 'CreateView' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return {name: 'main'}
  }
})

router.beforeEach((to, from) => {
  const store = useAuthStore()
  if (to.name === 'friend' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return {name: 'main'}
  }
})



export default router
