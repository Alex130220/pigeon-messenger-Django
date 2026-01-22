import os
import re

# Файлы для проверки и исправления
FILES_TO_CHECK = [
    'users/admin.py',
    'messenger/models.py',
    'notifications/models.py',
    'messenger/views.py',
    'users/views.py',
    'pigeon/urls.py',
]

def fix_user_imports():
    """Исправляет импорты пользователей во всех файлах"""
    print("🔧 Исправление импортов пользователей...")
    
    for file_path in FILES_TO_CHECK:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Исправляем импорты CustomUser
        if 'from .models import CustomUser' in content:
            content = content.replace(
                'from .models import CustomUser',
                '# from .models import CustomUser  # Временно отключено'
            )
            print(f"  ✅ Исправлен импорт в {file_path}")
        
        # Исправляем get_user_model если нужно
        if 'get_user_model' in content and 'User = get_user_model()' in content:
            # Добавляем альтернативный вариант
            content = content.replace(
                'from django.contrib.auth import get_user_model\nUser = get_user_model()',
                '''# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.conf import settings
User = settings.AUTH_USER_MODEL'''
            )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  📝 Файл {file_path} обновлен")
    
    print("✅ Все импорты исправлены!")

if __name__ == '__main__':
    fix_user_imports()