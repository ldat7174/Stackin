from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

# Thông tin phòng chat
class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_rooms/', blank=True, null=True)
    
    def __str__(self):
        return self.name or f"ChatRoom {self.id}"

# Thông tin liên hệ (danh bạ)
class Contact(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts_owned')
    contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_blocked = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    
    class Meta:
        # Đảm bảo mỗi owner chỉ có một liên hệ với một contact nhất định
        unique_together = ('owner', 'contact')
    def __str__(self):
        return f"{self.owner.username} - {self.contact.username}" if self.contact else f"Contact {self.id}"

# Thông tin cuộc trò chuyện
class Conversation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Conversation in {self.chat_room.name} with {self.participants.count()} participants" if self.chat_room else f"Conversation {self.id}"

# Tin nhắn
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True) 
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} in {self.conversation.chat_room.name if self.conversation.chat_room else 'No ChatRoom'}"

#Trạng thái tin nhắn
class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Đảm bảo mỗi tin nhắn chỉ có một trạng thái cho mỗi người dùng
        unique_together = ('message', 'user')

    def __str__(self):
        return f"Status of {self.message.id} for {self.user.username} - Read: {self.is_read}, Delivered: {self.is_delivered}"
