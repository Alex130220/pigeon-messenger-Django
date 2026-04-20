# users/admin.py
"""
ВНИМАНИЕ: Этот файл временно отключен для работы на Render.
Модель User уже зарегистрирована Django автоматически.
"""

import os

# Определяем, работаем ли мы на Render
IS_RENDER = 'RENDER' in os.environ

if IS_RENDER:
    # НА RENDER: используем стандартную модель
    print("=" * 60)
    print("🐦 PIGEON MESSENGER - RENDER MODE")
    print("Используется стандартная модель auth.User")
    print("Модель уже зарегистрирована Django")
    print("=" * 60)
    
    # НИЧЕГО НЕ РЕГИСТРИРУЕМ!
    # Модель User уже зарегистрирована Django по умолчанию
    
else:
    # ЛОКАЛЬНО: пытаемся использовать CustomUser
    try:
        from django.contrib import admin
        from django.contrib.auth.admin import UserAdmin
        from .models import CustomUser
        
        class CustomUserAdmin(UserAdmin):
            list_display = ('username', 'email', 'first_name', 'last_name', 'position')
            fieldsets = UserAdmin.fieldsets + (
                ('Дополнительная информация', {'fields': ('position', 'phone')}),
            )
        
        admin.site.register(CustomUser, CustomUserAdmin)
        print("✅ Локально: Используется кастомная модель CustomUser")
        
    except ImportError:
        # Если CustomUser не существует, ничего не делаем
        print("⚠️ Локально: CustomUser не найден, используем стандартную модель")
