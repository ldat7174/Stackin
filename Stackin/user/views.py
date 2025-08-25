from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, status
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from .models import User


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    "user": serializer.data,
                    "message": "Đăng ký thành công!"
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = serializer.create_token(user)
            user_data = UserSerializer(user, context={"request": request}).data
            return Response({
                'user': user_data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user  
        serializer = UserSerializer(user)  
        return Response(serializer.data)

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user 

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Cập nhật thành công",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)