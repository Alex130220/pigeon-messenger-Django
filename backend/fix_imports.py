# fix_all_imports.py
import os
import re

print("🔧 ИСПРАВЛЕНИЕ ВСЕХ ИМПОРТОВ В ПРОЕКТЕ")
print("=" * 60)

def fix_file(file_path):
    """Исправляет импорты в одном файле"""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = False
    
    # Паттерны для поиска и замены
    patterns = [
        # 1. Импорты CustomUser из users.models
        (r'from\s+users\.models\s+import\s+CustomUser',
         'from django.conf import settings\nUser = settings.AUTH_USER_MODEL'),
        
        # 2. Импорты CustomUser из .models (относительный импорт)
        (r'from\s+\.models\s+import\s+CustomUser',
         'from django.conf import settings\nUser = settings.AUTH_USER_MODEL'),
        
        # 3. Импорты get_user_model
        (r'from\s+django\.contrib\.auth\s+import\s+get_user_model',
         'from django.conf import settings\nUser = settings.AUTH_USER_MODEL'),
        
        # 4. User = get_user_model() на одной строке
        (r'User\s*=\s*get_user_model\(\)',
         'from django.conf import settings\nUser = settings.AUTH_USER_MODEL'),
        
        # 5. Импорты CustomUser в списке импортов
        (r'import\s+CustomUser',
         ''),
    ]
    
    for pattern, replacement in patterns:
        if re.search(pattern, content, re.MULTILINE):
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            changes_made = True
    
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Исправлен: {file_path}")
        return True
    
    return False

# Находим ВСЕ Python файлы в проекте
python_files = []
for root, dirs, files in os.walk('.'):
    # Пропускаем виртуальные окружения и скрытые папки
    if '.venv' in root or '__pycache__' in root or '.git' in root:
        continue
    
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))

print(f"📁 Найдено {len(python_files)} Python файлов")
print()

# Исправляем каждый файл
fixed_count = 0
for file_path in python_files:
    if fix_file(file_path):
        fixed_count += 1

print()
print("=" * 60)
print(f"✅ ИСПРАВЛЕНО: {fixed_count} файлов")
print("=" * 60)
print()
print("📋 Список основных файлов, которые нужно проверить:")
print("1. messenger/serializers.py")
print("2. messenger/models.py")
print("3. notifications/models.py")
print("4. pigeon/views.py")
print("5. users/views.py")
print("6. users/admin.py")
print()

# Создаем исправленный messenger/serializers.py
print("🛠️  Создаем исправленный messenger/serializers.py...")
serializers_content = '''# messenger/serializers.py
from rest_framework import serializers
from django.conf import settings

User = settings.AUTH_USER_MODEL
from .models import Message, Conversation, ChatRoom, Department, Tag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'recipient', 'timestamp', 
                 'is_read', 'is_edited', 'message_type', 'parent', 'tags']
        read_only_fields = ['timestamp', 'is_read', 'is_edited']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'last_message']
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

class ChatRoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'members', 'created_at']
'''

with open('messenger/serializers.py', 'w', encoding='utf-8') as f:
    f.write(serializers_content)
print("✅ messenger/serializers.py создан")

# Создаем исправленный messenger/models.py
print("🛠️  Создаем исправленный messenger/models.py...")
models_content = '''# messenger/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

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
'''

with open('messenger/models.py', 'w', encoding='utf-8') as f:
    f.write(models_content)
print("✅ messenger/models.py создан")

print()
print("🎉 ВСЕ ИМПОРТЫ ИСПРАВЛЕНЫ!")
print("Теперь проект использует settings.AUTH_USER_MODEL вместо прямых импортов.")
