from rest_framework import serializers
from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"   # hoặc chọn cụ thể ['id', 'title', 'content', 'description', 'report_type', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('report_type') not in ['bug', 'feature_request', 'other']:
            raise serializers.ValidationError("Loại báo cáo không hợp lệ.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
