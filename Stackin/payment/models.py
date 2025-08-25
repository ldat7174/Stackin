from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)    
    payment_method = models.CharField(max_length=50, choices=(('credit_card','Credit Card'),('paypal','PayPal'),('bank_transfer','Bank Transfer')), default='credit_card')
    status = models.CharField(max_length=10, choices=(('pending','Pending'),('completed','Completed'),('failed','Failed')), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # lưu lần tạo đầu tiên
    updated_at = models.DateTimeField(auto_now=True)      # lưu lần chỉnh sửa cuối cùng
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
