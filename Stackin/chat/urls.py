from django.urls import path
from .views import ChatRoomView, MessageView, ConversationView, ContactView, MessageStatusView


urlpatterns = [
    path('chatroom/<int:pk>/', ChatRoomView.as_view(), name='chat_room'),
    path('message/<int:pk>/', MessageView.as_view(), name='message_detail'),
    path('conversation/<int:pk>/', ConversationView.as_view(), name='conversation_detail'),
    path('contact/<int:pk>/', ContactView.as_view(), name='contact_detail'),
    path('message/status/<int:pk>/', MessageStatusView.as_view(), name='message_status_detail'),
]