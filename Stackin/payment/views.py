from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from payment.models import Payment
from payment.serializers import PaymentSerializer
import time


class PaymentView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        start = time.time()
        payments = Payment.objects.filter(user=self.request.user)
        serializer = PaymentSerializer(payments, many=True)
        try:
            response = Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        end = time.time()
        print(f"Thời gian xử lý: {end - start} giây")
        return response

    def post(self, request):
        start = time.time()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        end = time.time()
        print(f"Thời gian xử lý: {end - start} giây")
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


