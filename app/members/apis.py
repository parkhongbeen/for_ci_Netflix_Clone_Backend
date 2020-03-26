from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import User, Profile
from members.serializers import UserCreateSerializer, UserDetailSerializer, ProfileDetailSerializer, \
    ProfileCreateSerializer


# 로그인
class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
        else:
            raise AuthenticationFailed()

        serializer = UserDetailSerializer(user)
        return Response(serializer.data)


# 로그아웃하면 서버에서 삭제
# 로그아웃
class UserLogoutAPIView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# 회원가입
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)


# profile 생성, profile list 처리
class ProfileListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileDetailSerializer
        return ProfileCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)