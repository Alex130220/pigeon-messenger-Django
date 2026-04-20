# users/models.py
"""
ВНИМАНИЕ: Временно отключена кастомная модель пользователя.

Исходный код (закомментирован для истории):

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+999999999'")
    
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Должность')
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[phone_regex],
        verbose_name='Телефон')

    department = models.ForeignKey(
        'messenger.Department', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return self.get_full_name() or self.username

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}".strip()
"""

# Временно оставляем файл пустым
# Мы используем стандартную модель auth.User
# Это позволит запустить проект на Render без ошибок

print("ℹ️  Используется стандартная модель auth.User")
