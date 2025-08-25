from rest_framework import serializers
from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs.get('amount') <= 0:
            raise serializers.ValidationError("Số tiền thanh toán phải lớn hơn 0.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
