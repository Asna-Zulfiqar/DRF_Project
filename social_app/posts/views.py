from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.filters import PostFilter
from posts.models import Post , Comment
from posts.serializers import PostSerializer , CommentSerializer

class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        post = super().get_object()
        # Check if the logged-in user is the owner of the post for updates and deletions
        if self.request.method in ['PUT', 'DELETE'] and post.owner != self.request.user:
            raise PermissionDenied('You do not have permission to modify this post.')
        return post

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        # Increment views when the post is viewed
        post.increment_views()

        # Serialize the post data
        serializer = self.get_serializer(post)
        # Include statistics in the response
        data = serializer.data
        data['likes_count'] = post.like_count()
        data['dislikes_count'] = post.dislike_count()
        data['comments_count'] = post.comment_count()
        data['views_count'] = post.view_count()
        data['impressions_count'] = post.impression_count()

        return Response(data)

class LikeUnlikeDislikeCommentPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, action):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=404)

        if action == 'like':
            if request.user in post.likes.all():
                return Response({'message': 'You have already liked this post'}, status=400)
            post.likes.add(request.user)
            return Response({'message': 'Post liked successfully'}, status=201)

        elif action == 'unlike':
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                return Response({'message': 'Post unliked successfully'}, status=200)
            return Response({'message': 'You have not liked this post'}, status=400)

        elif action == 'dislike':
            if request.user in post.dislikes.all():
                return Response({'message': 'You have already disliked this post'}, status=400)
            # Add user to dislikes
            post.dislikes.add(request.user)
            return Response({'message': 'Post disliked successfully'}, status=201)

        elif action == 'comment':
            if request.user in post.comments.all():
                return Response({'message': 'You have already commented this post'}, status=400)
            comment_body = request.data.get('body')
            if not comment_body:
                return Response({'error': 'Comment body is required'}, status=400)

            # Create and save the comment
            comment = Comment.objects.create(
                body=comment_body,
                post=post,
                user=request.user
            )

            # Serialize the comment
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data, status=201)
        return Response({'error': 'Invalid action'}, status=400)


class FilteredPostView(APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        filter_params = self.request.data
        return PostFilter(filter_params, queryset=Post.objects.all()).qs

    def post(self, request, *args, **kwargs):
        filtered_posts = self.get_queryset()
        serializer = self.serializer_class(filtered_posts, many=True)
        return Response(serializer.data, status=200)