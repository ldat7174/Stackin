from rest_framework import serializers
from django.contrib.auth.models import User
from chat.models import Message, ChatRoom, Conversation, MessageStatus, Contact

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ['id', 'username', 'email']

    def validate(self, attrs):
        if 'username' in attrs and User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Tên người dùng đã tồn tại.")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)

    class Meta: 
        model = ChatRoom
        fields = ["id", "name", "is_group", "members", "created_at", "update_at"]
        read_only_fields = ['created_at', 'updated_at']

        def validate(self, attrs):
            if attrs.get('is_group') and not attrs.get('name'):
                raise serializers.ValidationError("Tên phòng chat nhóm không được để trống.")
            return attrs

        def create(self, validated_data):
            user = self.context['request'].user
            validated_data['members'] = user
            return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp"]
        read_only_fields = ['timestamp']
        extra_kwargs = {
            'room': {'required': True},
            'sender': {'read_only': True}
        }

        def validate(self, attrs):
            if not attrs.get('content'):
                raise serializers.ValidationError("Nội dung tin nhắn không được để trống.")
            return attrs

        def create(self, validated_data):
            user = self.context['request'].user
            validated_data['sender'] = user
            return super().create(validated_data)

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "name", "participants", "created_at", "updated_at"]
        read_only_fields = ['created_at', 'updated_at']   

    def validate(self, attrs):
        if not attrs.get('chat_room'):
            raise serializers.ValidationError("Phòng chat không được để trống.")
        if not attrs.get('participants'):
            raise serializers.ValidationError("Tham gia không được để trống.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['participants'] = user
        return super().create(validated_data)

class MessageStatusSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = MessageStatus
        fields = ["id", "message", "user", "is_delivered", "is_read", "create_at", "updated_at"]
        read_only_fields = ['updated_at', 'created_at']

    def validate(self, attrs):
        if not attrs.get('message'):
            raise serializers.ValidationError("Tin nhắn không được để trống.")
        if not attrs.get('user'):
            raise serializers.ValidationError("Người dùng không được để trống.")
        return attrs 

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class ContactSerializer(serializers.ModelSerializer):
    contact = UserSerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ["id", "owner", "contact", "is_blocked", "created_at", "updated_at"]
        read_only_fields = ['created_at', 'updated_at', 'owner', 'contact']
        extra_kwargs = {'is_blocked': {'required': False}}

    def validate(self, attrs):
        # Kiểm tra contact và owner
        if not attrs.get('contact'):
            raise serializers.ValidationError("Liên hệ không được để trống.")
        if not attrs.get('owner'):
            raise serializers.ValidationError("Chủ sở hữu không được để trống.")
        # Kiểm tra chặn
        if attrs.get('is_blocked') and not attrs.get('contact'):
            raise serializers.ValidationError("Không thể chặn một liên hệ không tồn tại.")
        return attrs

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

