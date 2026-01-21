from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'position')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('position', 'phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
