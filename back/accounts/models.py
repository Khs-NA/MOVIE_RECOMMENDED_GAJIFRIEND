from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='users' ,null=True)
    email = models.EmailField(null=True)
    nickname = models.CharField(max_length=100)
    age = models.CharField(null=True, max_length=100)
    genre = models.CharField(null=True, max_length=100)
    gender = models.CharField(null=True, max_length=10)
    location = models.CharField(null=True, max_length=50)
    longitude_x =  models.CharField(null=True, max_length=50)
    latitude_y = models.CharField(null=True, max_length=50)
    followings = models.ManyToManyField('self',symmetrical=False, related_name='followers' )


    # # 추가한 필드: nickname, profile_image, age, gender
    # email = models.EmailField(null=True)
    # nickname = models.CharField(max_length=50)
    # age = models.IntegerField()
    # profile_image = models.ImageField(
    #     blank=True,
    #     null=True,
    #     upload_to='profile_image/%Y/%m',
    # )
    
    # # 성별 선택지
    # MALE = 'M'
    # FEMALE = 'F'
    # GENDER_CHOICES = [
    #     (MALE, '남성'),
    #     (FEMALE, '여성'),
    # ]
    # gender = models.CharField(
    #     max_length=1,
    #     choices=GENDER_CHOICES,
    # )

    # genre = models.CharField(max_length=50, blank=True)
    
    # def __str__(self):
    #     return self.username
