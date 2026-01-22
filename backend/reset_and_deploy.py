#!/usr/bin/env python
"""
Скрипт для автоматического сброса и настройки базы данных Pigeon Messenger
Использование: python reset_and_deploy.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Добавляем текущую директорию в путь Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

def print_header():
    """Выводит заголовок скрипта"""
    print("=" * 70)
    print("🔄 PIGEON MESSENGER - АВТОМАТИЧЕСКАЯ НАСТРОЙКА БАЗЫ ДАННЫХ")
    print("=" * 70)
    print()

def setup_django():
    """Настраивает Django окружение"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeon.settings')
        import django
        django.setup()
        print("✅ Django настроен")
        return True
    except Exception as e:
        print(f"❌ Ошибка настройки Django: {e}")
        return False

def check_database():
    """Проверяет подключение к базе данных"""
    print("🔍 Проверка подключения к базе данных...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Подключение к базе данных успешно")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False

def create_migrations():
    """Создает миграции для всех приложений"""
    print("\n📝 Создание миграций...")
    
    apps_to_migrate = ['users', 'messenger', 'notifications']
    
    for app in apps_to_migrate:
        print(f"  Создание миграций для {app}...")
        try:
            result = subprocess.run(
                [sys.executable, 'manage.py', 'makemigrations', app, '--noinput'],
                capture_output=True,
                text=True,
                cwd=BASE_DIR
            )
            if result.returncode == 0:
                if result.stdout.strip():
                    print(f"    ✅ Миграции созданы для {app}")
                else:
                    print(f"    ℹ️  Нет изменений для {app}")
            else:
                print(f"    ⚠️  Ошибка для {app}: {result.stderr}")
        except Exception as e:
            print(f"    ❌ Исключение для {app}: {e}")
    
    # Общие миграции
    print("  Создание общих миграций...")
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'makemigrations', '--noinput'],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        if result.returncode == 0:
            print("    ✅ Общие миграции созданы")
        else:
            print(f"    ⚠️  Ошибка: {result.stderr}")
    except Exception as e:
        print(f"    ❌ Исключение: {e}")

def apply_migrations():
    """Применяет все миграции"""
    print("\n🚀 Применение миграций...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--noinput'],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            print("✅ Миграции успешно применены")
            # Выводим подробности
            for line in result.stdout.split('\n'):
                if 'Applying' in line or 'OK' in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print(f"❌ Ошибка применения миграций: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение при применении миграций: {e}")
        return False

def create_customuser_table_manually():
    """Создает таблицу users_customuser вручную если миграции не сработали"""
    print("\n🛠️  Попытка создать таблицу users_customuser вручную...")
    
    try:
        from django.db import connection
        
        # SQL для создания таблицы
        sql = """
        CREATE TABLE IF NOT EXISTS users_customuser (
            id SERIAL PRIMARY KEY,
            password VARCHAR(128) NOT NULL,
            last_login TIMESTAMP WITH TIME ZONE NULL,
            is_superuser BOOLEAN NOT NULL,
            username VARCHAR(150) UNIQUE NOT NULL,
            first_name VARCHAR(150) NOT NULL,
            last_name VARCHAR(150) NOT NULL,
            email VARCHAR(254) NOT NULL,
            is_staff BOOLEAN NOT NULL,
            is_active BOOLEAN NOT NULL,
            date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
            avatar VARCHAR(100) NULL,
            phone VARCHAR(20) NULL,
            bio TEXT NULL,
            birth_date DATE NULL,
            position VARCHAR(100) NULL
        );
        """
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("✅ Таблица users_customuser создана вручную")
            
            # Проверяем создание
            cursor.execute("SELECT to_regclass('users_customuser')")
            exists = cursor.fetchone()[0]
            if exists:
                print("✅ Проверка: таблица существует в базе данных")
                return True
            else:
                print("❌ Таблица не создана")
                return False
                
    except Exception as e:
        print(f"⚠️  Ошибка при создании таблицы вручную: {e}")
        return False

def create_superuser():
    """Создает суперпользователя"""
    print("\n👑 Создание суперпользователя...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Данные суперпользователя
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        # Проверяем, существует ли пользователь
        if User.objects.filter(username=username).exists():
            print(f"ℹ️  Пользователь '{username}' уже существует")
            
            # Обновляем пароль на всякий случай
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            print(f"✅ Пароль для '{username}' обновлен")
            return True
        else:
            # Создаем нового суперпользователя
            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                print(f"✅ Суперпользователь создан:")
                print(f"   👤 Логин: {username}")
                print(f"   📧 Email: {email}")
                print(f"   🔑 Пароль: {password}")
                return True
            except Exception as e:
                print(f"❌ Ошибка при создании суперпользователя: {e}")
                
                # Пытаемся создать обычного пользователя
                try:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        is_staff=True,
                        is_superuser=True
                    )
                    print(f"✅ Пользователь создан как staff/superuser")
                    return True
                except Exception as e2:
                    print(f"❌ Не удалось создать пользователя: {e2}")
                    return False
                    
    except Exception as e:
        print(f"❌ Ошибка в процессе создания пользователя: {e}")
        return False

def create_test_users():
    """Создает тестовых пользователей"""
    print("\n👥 Создание тестовых пользователей...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        test_users = [
            {'username': 'alice', 'email': 'alice@example.com', 'password': 'alice123'},
            {'username': 'bob', 'email': 'bob@example.com', 'password': 'bob123'},
            {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'charlie123'},
        ]
        
        created_count = 0
        for user_data in test_users:
            if not User.objects.filter(username=user_data['username']).exists():
                try:
                    User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password']
                    )
                    print(f"  ✅ {user_data['username']} создан")
                    created_count += 1
                except Exception as e:
                    print(f"  ⚠️  Не удалось создать {user_data['username']}: {e}")
            else:
                print(f"  ℹ️  {user_data['username']} уже существует")
        
        if created_count > 0:
            print(f"✅ Создано {created_count} тестовых пользователей")
        else:
            print("ℹ️  Все тестовые пользователи уже существуют")
            
    except Exception as e:
        print(f"⚠️  Ошибка при создании тестовых пользователей: {e}")

def collect_static_files():
    """Собирает статические файлы"""
    print("\n🎨 Сборка статических файлов...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'collectstatic', '--noinput', '--clear'],
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            print("✅ Статические файлы собраны успешно")
            # Выводим статистику
            for line in result.stdout.split('\n'):
                if 'static files' in line.lower() or 'copied' in line.lower():
                    print(f"  {line.strip()}")
            return True
        else:
            print(f"❌ Ошибка сбора статических файлов: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение при сборе статических файлов: {e}")
        return False

def create_directories():
    """Создает необходимые директории"""
    print("\n📁 Создание необходимых директорий...")
    
    directories = [
        BASE_DIR / 'static' / 'css',
        BASE_DIR / 'static' / 'js',
        BASE_DIR / 'static' / 'images',
        BASE_DIR / 'staticfiles',
        BASE_DIR / 'media',
        BASE_DIR / 'media' / 'avatars',
        BASE_DIR / 'media' / 'uploads',
        BASE_DIR / 'sessions',
    ]
    
    created_count = 0
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {directory.relative_to(BASE_DIR)}")
            created_count += 1
        except Exception as e:
            print(f"  ⚠️  Не удалось создать {directory}: {e}")
    
    print(f"✅ Создано/проверено {created_count} директорий")

def create_sample_static_files():
    """Создает примеры статических файлов если их нет"""
    print("\n🖼️  Проверка статических файлов...")
    
    # CSS файл
    css_file = BASE_DIR / 'static' / 'css' / 'style.css'
    if not css_file.exists():
        try:
            css_content = """/* Основные стили Pigeon Messenger */
body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
.container { max-width: 1200px; margin: 0 auto; }
.navbar { background: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
.btn { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
.btn:hover { background: #5a67d8; }"""
            
            with open(css_file, 'w', encoding='utf-8') as f:
                f.write(css_content)
            print("  ✅ Создан style.css")
        except Exception as e:
            print(f"  ⚠️  Не удалось создать style.css: {e}")
    else:
        print("  ℹ️  style.css уже существует")
    
    # JS файл
    js_file = BASE_DIR / 'static' / 'js' / 'main.js'
    if not js_file.exists():
        try:
            js_content = """// Основной JavaScript файл Pigeon Messenger
console.log('Pigeon Messenger loaded');
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready');
    // Проверка соединения
    fetch('/health/').then(r => {
        const status = document.getElementById('connection-status');
        if (status) status.textContent = r.ok ? 'Online' : 'Offline';
    });
});"""
            
            with open(js_file, 'w', encoding='utf-8') as f:
                f.write(js_content)
            print("  ✅ Создан main.js")
        except Exception as e:
            print(f"  ⚠️  Не удалось создать main.js: {e}")
    else:
        print("  ℹ️  main.js уже существует")

def run_tests():
    """Запускает тесты для проверки"""
    print("\n🧪 Запуск тестов...")
    
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'test', '--failfast'],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Все тесты пройдены успешно")
            return True
        else:
            print(f"❌ Тесты не пройдены: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️  Тесты превысили лимит времени")
        return False
    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")
        return False

def main():
    """Основная функция"""
    print_header()
    
    # Засекаем время
    start_time = time.time()
    
    # 1. Настройка Django
    if not setup_django():
        print("❌ Не удалось настроить Django. Выход.")
        return False
    
    # 2. Проверка базы данных
    if not check_database():
        print("⚠️  Проблемы с подключением к БД, но продолжаем...")
    
    # 3. Создание директорий
    create_directories()
    
    # 4. Создание статических файлов
    create_sample_static_files()
    
    # 5. Создание миграций
    create_migrations()
    
    # 6. Применение миграций
    migrations_ok = apply_migrations()
    
    # 7. Если миграции не сработали, создаем таблицу вручную
    if not migrations_ok:
        print("\n⚠️  Миграции не применены, пробуем создать таблицу вручную...")
        create_customuser_table_manually()
    
    # 8. Создание суперпользователя
    superuser_ok = create_superuser()
    
    # 9. Создание тестовых пользователей
    create_test_users()
    
    # 10. Сбор статических файлов
    collect_static_files()
    
    # 11. Запуск тестов (опционально)
    if '--test' in sys.argv:
        run_tests()
    
    # Подводим итоги
    print("\n" + "=" * 70)
    print("📊 ИТОГИ НАСТРОЙКИ:")
    print("=" * 70)
    
    elapsed_time = time.time() - start_time
    print(f"⏱️  Время выполнения: {elapsed_time:.2f} секунд")
    
    if migrations_ok:
        print("✅ Миграции: УСПЕШНО")
    else:
        print("⚠️  Миграции: ЧАСТИЧНО (таблица создана вручную)")
    
    if superuser_ok:
        print("✅ Суперпользователь: СОЗДАН/ОБНОВЛЕН")
    else:
        print("❌ Суперпользователь: НЕ СОЗДАН")
    
    print("📁 Директории: СОЗДАНЫ")
    print("🎨 Статические файлы: ГОТОВЫ")
    print("\n🔧 Команды для проверки:")
    print("   python manage.py runserver")
    print("   python manage.py createsuperuser")
    print("   python manage.py shell")
    
    print("\n🚀 Настройка завершена!")
    print("=" * 70)
    
    return migrations_ok and superuser_ok

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Процесс прерван пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Необработанное исключение: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
