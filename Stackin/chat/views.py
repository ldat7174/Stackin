from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import ChatRoom, Contact, Conversation, Message, MessageStatus
from .serializers import ChatRoomSerializer, ContactSerializer, ConversationSerializer, MessageSerializer, MessageStatusSerializer
import time


# View for ChatRoom
class ChatRoomView(APIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start = time.time()
        chatrooms = ChatRoom.objects.filter(members=self.request.user)
        serializer = ChatRoomSerializer(chatrooms, many=True)
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
        serializer.save()

# View for Contact
class ContactView(APIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start = time.time()
        contacts = Contact.objects.filter(user=self.request.user)
        serializer = ContactSerializer(contacts, many=True)
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

# View for Conversation
class ConversationView(APIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start = time.time()
        conversations = Conversation.objects.filter(participants=self.request.user)
        serializer = ConversationSerializer(conversations, many=True)
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
        serializer.save()

# View for Message
class MessageView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start = time.time()
        messages = Message.objects.filter(sender=self.request.user)
        serializer = MessageSerializer(messages, many=True)
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
        serializer.save(sender=self.request.user)

# View for MessageStatus
class MessageStatusView(APIView):
    serializer_class = MessageStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        start = time.time()
        statuses = MessageStatus.objects.filter(user=self.request.user)
        serializer = MessageStatusSerializer(statuses, many=True)
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