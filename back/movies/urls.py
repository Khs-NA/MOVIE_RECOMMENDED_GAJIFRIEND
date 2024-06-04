from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list), # 영화 리스트
    path('movies/new/', views.movie_list_new), # 영화 리스트
    path('movies/call/',views.movie_list_call),
    # path('movies/',views.movie_list_call),
    path('movies/<int:movie_id>/like/', views.like_movie), # 영화 좋아요 기능
    # path('movies/recommend/', views.recommend_movies), # 영화 추천??
    path('movies/top-rated/', views.get_top_rated_movies), # 영화 추천??
    path('user/liked/', views.liked_movies), # 유저가 좋아요 누른 영화 추천
    # path('genres/', views.genre_list) # 장르 가져오기
]

