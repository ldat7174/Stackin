from rest_framework import serializers
from .models import User, IdentityVerification, TaskerRegistration
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:  
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "phone", "gender", "birthday", "avatar",
            "is_verified", "is_tasker"
        ]
        read_only_fields = ["id", "is_verified", "is_tasker"]

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar_url) 
        return None

class RegisterSerializer(serializers.ModelSerializer):  
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'phone', 'gender', 'birthday']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Mật khẩu không khớp!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user 

class IdentityVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityVerification
        fields = [
            "id", "user", "id_number", "front_image", "back_image",
            "status", "reason", "submitted_at"
        ]
        read_only_fields = ["id", "status", "reason", "submitted_at"]

class TaskerRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskerRegistration
        fields = [
            "id", "user", "bio", "experience",
            "agreed_terms", "status", "submitted_at"
        ]
        read_only_fields = ["id", "status", "submitted_at"]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data): 
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Email không tồn tại")

            user = authenticate(username=user.username, password=password)
            if not user:
                raise serializers.ValidationError("Mật khẩu không đúng")
        else:
            raise serializers.ValidationError("Vui lòng nhập email và mật khẩu")

        data['user'] = user
        return data

    def create_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "gender", "birthday", "avatar",]  # tùy theo model bạn có
        extra_kwargs = {f: {"required": False} for f in fields}

