from django.urls import path
from . import views

urlpatterns  = [
    path('' , views.post_list, name='post_list'),
    path('<int:post_id>' , views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/unlike/', views.unlike_post, name='unlike_post'),
    path('filter/', views.get_filtered_posts, name='get_filtered_posts'),
]