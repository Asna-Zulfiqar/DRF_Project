from django.urls import path
from users.views import (UserListCreateView, UserDetailView,
                         FollowUserView, UnFollowUser, BlockUser, UnBlockUser)

urlpatterns  = [
    path('' , UserListCreateView.as_view(), name='user_list'),
    path('detail/' , UserDetailView.as_view(), name='user_detail'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnFollowUser.as_view(), name='unfollow_user'),
    path('block/<int:user_id>/', BlockUser.as_view(), name='block_user'),
    path('unblock/<int:user_id>/', UnBlockUser.as_view(), name='unblock_user'),
]