from django.urls import path
from . import views

urlpatterns  = [
    path('' , views.user_list, name='user_list'),
    path('<int:user_id>' , views.user_detail, name='user_detail'),
    path('<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('<int:user_id>/block/', views.block_user, name='block_user'),
    path('<int:user_id>/unblock/', views.unblock_user, name='unblock_user'),
]