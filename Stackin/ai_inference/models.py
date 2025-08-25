from django.db import models

class InferenceRequest(models.Model):
    input_text = models.TextField()
    prediction = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inference: {self.input_text[:30]}..."
