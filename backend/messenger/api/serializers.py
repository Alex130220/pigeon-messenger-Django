from rest_framework import serializers
from messenger.models import Message  # Импорт из основного приложения

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'timestamp', 'room']
