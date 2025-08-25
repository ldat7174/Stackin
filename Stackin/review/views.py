from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from review.models import Review
from review.serializers import ReviewSerializer

class ProductView(APIView):
    permission_classes = [permissions.AllowAny]

class ReviewView(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get(self):
        reviews = Review.objects.filter(user=self.request.user)
        serializer = ReviewSerializer(reviews, many=True)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            review = Review.objects.get(pk=pk, user=request.user)
        except Review.DoesNotExist:
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
