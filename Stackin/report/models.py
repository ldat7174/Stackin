from django.db import models
from django.conf import settings


class Report(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50, choices=[
        ('bug', 'Bug'),
        ('feature_request', 'Feature Request'),
        ('other', 'Other')
    ])
    status = models.CharField(max_length=50, default='open', choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.report_type} by {self.created_by.username}"

