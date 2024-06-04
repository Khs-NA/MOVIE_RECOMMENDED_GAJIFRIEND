from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
 # 필요한 필드들을 추가합니다.
    nickname = serializers.CharField(
    required=False,
    allow_blank=True,
    max_length=255
    )

    image = serializers.ImageField(required=False)
    age = serializers.CharField(required=False )
    genre = serializers.CharField(required=False )
    gender = serializers.CharField(required=False )
    location = serializers.CharField(required=False )
    longitude_x = serializers.CharField(required=False )
    latitude_y = serializers.CharField(required=False )
    

    # 해당 필드도 저장 시 함께 사용하도록 설정합니다.
    def get_cleaned_data(self):
        return {
        'username': self.validated_data.get('username', ''),
        'password1': self.validated_data.get('password1', ''),
        # nickname 필드 추가
        'image': self.validated_data.get('image', ''),
        'nickname': self.validated_data.get('nickname', ''),
        'age': self.validated_data.get('age', ''),
        'genre': self.validated_data.get('genre', ''),
        'gender': self.validated_data.get('gender', ''),
        'location': self.validated_data.get('location', ''),
        'longitude_x': self.validated_data.get('longitude_x', ''),
        'latitude_y': self.validated_data.get('latitude_y', ''),
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('pk', 'username','image', 'nickname', 'age', 'genre', 'gender', 'location', 'longitude_x', 'latitude_y','followings')
        read_only_fields = ('email',)
