from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from users.models import CustomUser
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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


class UserListCreateView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = request.user  # Authenticated user
        following_user = get_object_or_404(CustomUser, pk=user_id)

        if user == following_user:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.following.filter(id=following_user.id).exists():
            return Response(
                {"error": f"You are already following {following_user.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.following.add(following_user)
        return Response(
            {"message": f"You are now following {following_user.username}."},
            status=status.HTTP_200_OK
        )


class UnFollowUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        following_user = get_object_or_404(CustomUser, pk=user_id)
        if user == following_user:
            return Response(
            {"error": "You cannot unfollow yourself."},
            status=status.HTTP_400_BAD_REQUEST
            )
        if not user.following.filter(id=following_user.id).exists():
            return Response(
                {"error": f"You are Not following {following_user.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.following.remove(following_user)
        return Response(
            {"message": f"You are now not following {following_user.username}."},
            status=status.HTTP_200_OK
        )


class BlockUser(APIView):
    permission_classes = ([IsAuthenticated])
    def post(self, request, user_id):
        user = request.user
        blocked_user = get_object_or_404(CustomUser, pk=user_id)
        if user == blocked_user:
            return Response({"message": "You cannot block yourself."}, status=400)
        if user.blocked_users.filter(id=blocked_user.id).exists():
            return Response(
                {"error": f"You are already following {blocked_user.username}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.blocked_users.add(blocked_user)
        return Response({"message": f"You have blocked {blocked_user.username}."} ,
                        status=status.HTTP_200_OK)

class UnBlockUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        blocked_user = get_object_or_404(CustomUser, pk=user_id)

        if not user.blocked_users.filter(id=blocked_user.id).exists():
            return Response({"message": f"You have not blocked {blocked_user.username}"}, status=400)

        user.blocked_users.remove(blocked_user)
        return Response({"message": f"You have unblocked {blocked_user.username}."})