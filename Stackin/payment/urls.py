from .views import PaymentView
from django.urls import path

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
]