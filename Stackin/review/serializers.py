from rest_framework import serializers
from review.models import Review, Product

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate(self, attrs):
        if attrs.get('rating') is not None and (attrs['rating'] < 1 or attrs['rating'] > 5):
            raise serializers.ValidationError("Đánh giá phải trong khoảng từ 1 đến 5.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class ProductSerializer(serializers.Serializer):
    class meta:
        model = Product
        fields = "name"

    def validate(self, attrs):
        if attrs.get('product') is None:
            raise serializers.ValidationError("Sản phẩm không tồn tại.")
        return attrs