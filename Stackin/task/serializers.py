from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('due_date') and attrs['due_date'] < attrs.get('created_at', None):
            raise serializers.ValidationError("Ngày hết hạn không thể trước ngày tạo.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'status' in validated_data and validated_data['status'] != instance.status:
            # Log trạng thái thay đổi ở đây nếu cần
            pass
        return super().update(instance, validated_data)
