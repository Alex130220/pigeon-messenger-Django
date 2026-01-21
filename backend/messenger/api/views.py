from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from messenger.models import Message
from .serializers import MessageSerializer

class MessageList(APIView):
    def get(self, request):
        messages = Message.objects.all().order_by('-timestamp')[:50]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
