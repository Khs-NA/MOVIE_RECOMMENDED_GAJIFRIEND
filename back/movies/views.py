# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Movie, Movie_New
from .serializers import MovieSerializer, NewMovieSerializer
import requests
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


genre_mapping = {
    12: "모험",
    14: "판타지",
    16: "애니메이션",
    18: "드라마",
    27: "공포",
    28: "액션",
    35: "코미디",
    36: "역사",
    37: "서부",
    53: "스릴러",
    80: "범죄",
    99: "다큐멘터리",
    878: "SF",
    9648: "미스터리",
    10402: "음악",
    10749: "로맨스",
    10751: "가족",
    10752: "전쟁",
    10770: "TV 영화"
}


# 현재 상영작 불러오기
@api_view(['GET'])
def movie_list_new(request):
    if request.method == 'GET':
        url = "https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&page=1&region=KR"
        headers = {
            "accept": "application/json",
            "Authorization": settings.VITE_TMDB_API_KEY
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            movies_data = response.json()['results']
            
            for movie_data in movies_data:
                genre_names = [genre_mapping[genre_id] for genre_id in movie_data['genre_ids'] if genre_id in genre_mapping]
                
                if 'overview' in movie_data and movie_data['overview'].strip() and \
                   'poster_path' in movie_data and movie_data['poster_path'].strip():
                    movie, created = Movie_New.objects.update_or_create(
                        title=movie_data['title'],
                        defaults={
                            'release_date': datetime.strptime(movie_data['release_date'], '%Y-%m-%d'),
                            'overview': movie_data['overview'],
                            'poster_path': movie_data['poster_path'],
                            'vote_average': movie_data['vote_average'],
                            'genres': ', '.join(genre_names)  # 장르 이름을 문자열로 저장
                        }
                    )

            movies = Movie_New.objects.all().order_by('-vote_average')
            serializer = NewMovieSerializer(movies, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Failed to fetch data from TMDB"}, status=response.status_code)




# @api_view(['GET'])
# def genre_list(request):

#     if request.method == 'GET':
#         url = "https://api.themoviedb.org/3/genre/movie/list?language=ko"
#         headers = {
#             "accept": "application/json",
#             "Authorization": "Authorization": settings.VITE_TMDB_API_KEY
#         }
#         response = requests.get(url, headers=headers)

#         if response.status_code == 200:
#             genres_data = response.json()['genres']
            
#             # 데이터베이스에 저장
#             for genre_data in genres_data:
#                 genre, created = Genre.objects.update_or_create(
#                     id=genre_data['id'],
#                     defaults={
#                         'name': genre_data['name'],
#                     }
#                 )

#             # 저장된 데이터를 반환
#             genres = Genre.objects.all()
#             serializer = GenreSerializer(genres, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({"error": "Failed to fetch data from TMDB"}, status=response.status_code)


# 영화 데이터 불러오기
@api_view(['GET'])
# @renderer_classes([JSONRenderer])
def movie_list_call(request):
    if request.method == 'GET':
        url = "https://api.themoviedb.org/3/discover/movie"
        headers = {
                "accept": "application/json",
                "Authorization": settings.VITE_TMDB_API_KEY
            }
        params = {
            "include_adult": "false",
            "include_video": "false",
            "language": "ko-KR",
            "region": "KR",
            "sort_by": "vote_average.desc",
            "vote_count.gte": "1000",
        }

        all_movies = []

        for page in range(1, 1000):  # 1부터 9까지 페이지를 반복 요청
            params['page'] = page
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                movies_data = response.json()['results']
                for movie_data in movies_data:
                    genre_names = [genre_mapping[genre_id] for genre_id in movie_data['genre_ids'] if genre_id in genre_mapping]
                    if 'overview' in movie_data and movie_data['overview'].strip() and \
                    'poster_path' in movie_data and movie_data['poster_path'].strip():
                        movie, created = Movie.objects.update_or_create(
                            title=movie_data['title'],
                            defaults={
                                'release_date': datetime.strptime(movie_data['release_date'], '%Y-%m-%d'),
                                'overview': movie_data['overview'],
                                'poster_path': movie_data['poster_path'],
                                'vote_average': movie_data['vote_average'],
                                'genres': ', '.join(genre_names)  # 장르 이름을 문자열로 저장
                            }
                        )
                        all_movies.append(movie)
                print(f"Processed page {page}")
            else:
                print(f"Failed to fetch data for page {page}, status code: {response.status_code}")
                continue  # 실패 시 다음 페이지로 계속

        movies = Movie.objects.all().order_by('-vote_average')
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def like_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user in movie.like_users.all():
        movie.like_users.remove(request.user)
    else:
        movie.like_users.add(request.user)
    return Response({'status': 'success'})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommend_movies(request):
#     user = request.user
#     liked_movies = user.like_movies.all()
#     recommended_movies = Movie.objects.filter(
#         genres__in=[movie.genres for movie in liked_movies]
#     ).distinct().exclude(id__in=liked_movies.values_list('id', flat=True))

#     serializer = MovieSerializer(recommended_movies, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request):
    user = request.user
    liked_movies = user.like_movies.all()
    serializer = MovieSerializer(liked_movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_top_rated_movies(request):
    top_rated_movies = Movie.objects.order_by('-vote_average')[:30]
    # Serialize and return the data
    serializer = MovieSerializer(top_rated_movies, many=True)
    return Response(serializer.data)


