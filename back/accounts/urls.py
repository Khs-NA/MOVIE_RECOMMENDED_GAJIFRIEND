from django.urls import path
from .views import UserProfileUpdateView
from . import views

urlpatterns = [
    path('user/profile/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('user/userlist/', views.user_list),
    path('user/follow/<int:user_pk>/', views.follow),
    path('user/follow/<int:user_pk>/status/', views.follow_status, name='follow_status'),
]
