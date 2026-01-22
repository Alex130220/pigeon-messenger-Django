# pigeon/apps.py
from django.apps import AppConfig

class PigeonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pigeon'
    verbose_name = 'Pigeon Messenger'
    
    def ready(self):
        """Вызывается при запуске приложения"""
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
            print("=" * 50)
            print("🐦 PIGEON MESSENGER")
            print("=" * 50)
            print("Статус: Запущен")
            print("Модель пользователя: Стандартная (auth.User)")
            print("Таблица: auth_user")
            print("Админка: /admin")
            print("Вход: admin / admin123")
            print("=" * 50)