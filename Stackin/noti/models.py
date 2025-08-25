from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=[('info', 'Information'), ('warning', 'Warning'), ('error', 'Error'), ('success', 'Success'),], default='info')
    related_object_id = models.PositiveIntegerField(null=True, blank=True)  # ID of the related object, if any
    related_object_type = models.CharField(max_length=50, null=True, blank=True)  # Type of the related object, if any

    def __str__(self):
        return f"Notification for {self.user.username} - {self.notification_type} - {self.message[:50]}"
