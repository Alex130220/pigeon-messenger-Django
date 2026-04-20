from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    SYSTEM = "system"
    MESSAGE_TYPES = [
        (TEXT, "Text"),
        (IMAGE, "Image"),
        (FILE, "File"),
        (SYSTEM, "System"),
    ]
    
    conversation = models.ForeignKey(
        Conversation, 
        related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, 
        related_name='sent_messages', 
        on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        User, 
        related_name="received_messages", 
        on_delete=models.CASCADE
    )
    chat_room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='Чат-комната'
    )
    content = models.TextField()
    message_type = models.CharField(
        max_length=10, 
        choices=MESSAGE_TYPES, 
        default=TEXT
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="replies"
    )
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["sender", "recipient"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["chat_room"]),
        ]

    def edit(self, new_content):
        self.content = new_content
        self.is_edited = True
        self.save()
        
    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.content[:20]}..."

  
