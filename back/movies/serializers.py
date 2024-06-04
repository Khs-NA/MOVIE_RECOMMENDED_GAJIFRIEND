from rest_framework import serializers
from .models import Movie, Movie_New

# 전체 영화
class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'

# 현재 상영작
class NewMovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie_New
        fields = '__all__'

# class GenreSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Genre
#         fields = '__all__'