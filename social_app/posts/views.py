from django.http import HttpResponse , JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from posts.models import Post  , Country
from posts.serializers import PostSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from posts.filters import  PostFilter


@api_view(['GET' , 'POST'])
def post_list(request):
    # Getting all Posts from Database
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

    # Creating New Post
    elif request.method == 'POST':

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication credentials were not provided.'}, status=403)

        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE' ])
@permission_classes([IsAuthenticated])
def post_detail(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return HttpResponse(status=404 , content='Post not found')

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':

        if post.owner != request.user:
            return JsonResponse({'error': 'You do not have permission to edit this post.'}, status=403)

        data = JSONParser().parse(request)
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data , status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if post.owner != request.user:
            return JsonResponse({'error': 'You do not have permission to delete this post.'}, status=403)
        post.delete()
        return HttpResponse(status=204 , content='Post deleted Successfully')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request , post_id):
    user = request.user
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    if post.likes.all():
        return Response({'message': 'You have already liked this post'}, status=400)

    post.likes.add(user)
    return Response({'message': 'Post liked successfully'}, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    user = request.user
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=404)

    if user in post.likes.all():
        post.likes.remove(user)
        return Response({'message': 'Post unliked successfully'}, status=200)
    else:
        return Response({'message': 'You have not liked this post'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_filtered_posts(request):
    filter_params = request.data  # The filter criteria sent in the request body

    # Use the PostFilter class to filter the posts
    filtered_posts = PostFilter(filter_params, queryset=Post.objects.all()).qs

    # Serialize and return the posts
    serializer = PostSerializer(filtered_posts, many=True)
    return Response(serializer.data, status=200)