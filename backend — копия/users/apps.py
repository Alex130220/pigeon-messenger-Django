# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи (Стандартные)'
    
    def ready(self):
        """
        Этот метод вызывается когда приложение готово.
        Можно добавить логику инициализации здесь.
        """
        print(f"✅ Приложение '{self.verbose_name}' загружено")
        print("   📝 Используется стандартная модель auth.User")
        print("   💡 Чтобы вернуть кастомную модель:")
        print("   1. Раскомментируйте код в users/models.py")
        print("   2. Установите AUTH_USER_MODEL = 'users.CustomUser' в settings.py")
        print("   3. Выполните миграции: python manage.py makemigrations users")
        print("   4. Примените миграции: python manage.py migrate users")

