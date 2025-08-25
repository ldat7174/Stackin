from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
import time


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = time.time()
        notis = Notification.objects.filter(user=request.user, is_read=False)
        serializer = NotificationSerializer(notis, many=True)
        try:
            response = Response(serializer.data, status=200)
        except Exception as e:
            response = Response({"error": str(e)}, status=400)
        end = time.time()
        print(f"Thời gian xử lý: {end - start} giây")
        return response

class NotificationMarkReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        start = time.time()
        try:
            noti = Notification.objects.get(pk=pk, user=request.user)
            noti.is_read = True
            noti.save()
            response = Response({"message": "Đã đánh dấu đã đọc"}, status=200)
        except Notification.DoesNotExist: 
            response = Response({"error": "Không tìm thấy thông báo"}, status=404) 
        end = time.time()
        print(f"Thời gian xử lý: {end - start} giây")
        return response
