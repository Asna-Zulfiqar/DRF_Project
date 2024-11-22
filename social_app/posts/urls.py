from django.urls import path
from .views import PostListCreateView, PostDetailView, FilteredPostView, \
    LikeUnlikeDislikeCommentPostView

urlpatterns  = [
    path('' , PostListCreateView.as_view(), name='post_list'),
    path('<int:id>/' , PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/<str:action>/', LikeUnlikeDislikeCommentPostView.as_view(), name='like_unlike_post'),
    path('filter/', FilteredPostView.as_view(), name='get_filtered_posts'),
]