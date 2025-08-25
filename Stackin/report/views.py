from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from report.models import Report
from report.serializers import ReportSerializer

class ReportAPIView(APIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self):
        report = Report.objects.filter(user=self.request.user).order_by("-created_at")
        serializer = ReportSerializer(report, many=True)
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Đảm bảo đã thêm trường 'user' trong serializer của Report
        serializer.save(user=self.request.user) 
