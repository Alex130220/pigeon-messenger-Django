# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

try:
    # Пробуем импортировать CustomUser
    from .models import CustomUser
    
    # Если CustomUser существует, регистрируем его
    class CustomUserAdmin(UserAdmin):
        # Добавьте кастомные поля, если нужно
        list_display = ('username', 'email', 'first_name', 'last_name', 'position', 'phone', 'is_staff')
        fieldsets = UserAdmin.fieldsets + (
            ('Дополнительная информация', {'fields': ('position', 'phone', 'department')}),
        )
    
    admin.site.register(CustomUser, CustomUserAdmin)
    print("✅ Используется кастомная модель CustomUser")
    
except ImportError:
    # Если CustomUser не существует, используем стандартную модель
    admin.site.register(User, UserAdmin)
    print("✅ Используется стандартная модель auth.User")
    print("💡 Для использования CustomUser раскомментируйте код в users/models.py")
