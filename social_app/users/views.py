from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
from .serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticating using the custom user model
        user = authenticate(username=username, password=password)

        if user:
            # If authentication is successful, generate and return the token
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            })
        return Response({'error': 'Invalid Credentials'}, status=400)

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_list(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Created Successfully', 'user_details': serializer.data}, status=201)
        return Response({'message': 'Validation failed', 'errors': serializer.errors}, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE' ])
@permission_classes([IsAuthenticated])
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Updated Successfully', 'user_details': serializer.data})
        return Response({'message': 'Validation failed', 'errors': serializer.errors}, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "User deleted Successfully"}, status=204)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user = request.user
    following_user = get_object_or_404(CustomUser, pk=user_id)

    if user == following_user:
        return Response({"message": "You cannot follow yourself."}, status=400)

    if user.following.filter(id=following_user.id).exists():
        return Response({"message": "You are already following this user"}, status=400)

    user.following.add(following_user)
    return Response({"message": f"You are now following {following_user.username}."})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user = request.user
    following_user = get_object_or_404(CustomUser, pk=user_id)

    if not user.following.filter(id=following_user.id).exists():
        return Response({"message": "You are not following this user"}, status=400)

    user.following.remove(following_user)
    return Response({"message": f"You have unfollowed {following_user.username}."}, status=204)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def block_user(request, user_id):
    user = request.user
    blocked_user = get_object_or_404(CustomUser, pk=user_id)

    if user == blocked_user:
        return Response({"message": "You cannot block yourself."}, status=400)

    if user.blocked_users.filter(id=blocked_user.id).exists():
        return Response({"message": "You have already blocked this user"}, status=400)

    user.blocked_users.add(blocked_user)
    return Response({"message": f"You have blocked {blocked_user.username}."})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unblock_user(request, user_id):
    user = request.user
    blocked_user = get_object_or_404(CustomUser, pk=user_id)

    if not user.blocked_users.filter(id=blocked_user.id).exists():
        return Response({"message": "You have not blocked this user"}, status=400)

    user.blocked_users.remove(blocked_user)
    return Response({"message": f"You have unblocked {blocked_user.username}."})
