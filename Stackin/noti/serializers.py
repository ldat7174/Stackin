from rest_framework import serializers
from noti.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("user", "created_at")

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Người dùng phải đăng nhập để tạo thông báo.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
