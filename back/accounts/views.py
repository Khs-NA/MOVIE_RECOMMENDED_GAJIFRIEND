from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import CustomUserDetailsSerializer
from rest_framework import status
from django.core.files.storage import default_storage
from django.conf import settings
import os
from .models import User
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, get_list_or_404
User = get_user_model()
from PIL import Image

class UserProfileUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # 이미지 처리
            image_file = request.FILES.get('image')
            if image_file:
                # 이미지 크기 조정
                image = Image.open(image_file)
                image.thumbnail((300, 300))  # 원하는 크기로 조정
                # 이미지 저장
                image_path = f"media/users/{user.id}_{user.username}.png"
                image.save(image_path)
                # serializer에 이미지 경로 업데이트
                serializer.validated_data['image'] = image_path

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomUserDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'image']  # 필요한 필드들 목록

#     def update(self, instance, validated_data):
#         if 'image' in validated_data:
#             file = validated_data.pop('image')
#             file_name = default_storage.save(file.name, file)
#             file_url = os.path.join(settings.MEDIA_URL, file_name)
#             instance.image = file_url  # 이미지 URL을 모델에 저장

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         instance.save()
#         return instance
# class UserProfileUpdateView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def put(self, request, *args, **kwargs):
#         user = request.user
#         # request.data에 파일이 포함되어 있을 수 있으므로 serializer에 전달
#         serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()  # serializer 내에서 파일 처리
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class UserProfileUpdateView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def put(self, request, *args, **kwargs):
#         user = request.user
#         serializer = CustomUserDetailsSerializer(user, data=request.data, partial=True)

#         if serializer.is_valid():
#             # 파일 처리
#             if 'image' in request.FILES:
#                 file = request.FILES['image']
#                 file_name = default_storage.save(file.name, file)
#                 file_url = os.path.join(settings.MEDIA_URL, file_name)
#                 user.image = file_url  # 이미지 URL을 모델에 저장

#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = CustomUserDetailsSerializer(users, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def follow(request, user_pk):
    follow_user = get_object_or_404(User, pk=user_pk)
    login_user = request.user
    if follow_user != login_user:  # 자신을 팔로우하지 못하도록 확인
        if login_user.followings.filter(pk=follow_user.pk).exists():
            login_user.followings.remove(follow_user)
            action = 'unfollowed'
        else:
            login_user.followings.add(follow_user)
            action = 'followed'
        return Response({'status': 'success', 'action': action})
    return Response({'status': 'failed', 'message': 'You cannot follow yourself'}, status=400)


@api_view(['GET'])
def follow_status(request, user_pk):
    follow_user = get_object_or_404(User, pk=user_pk)
    login_user = request.user
    is_following = login_user.followings.filter(pk=follow_user.pk).exists()
    return Response({'is_following': is_following})




