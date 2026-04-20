# force_create_table.py
import os
import django
from django.db import connection
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeon.settings')
django.setup()

print("🛠️  Принудительное создание таблиц...")

# Создаем таблицу users_customuser если она не существует
with connection.cursor() as cursor:
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_customuser (
                id SERIAL PRIMARY KEY,
                password VARCHAR(128) NOT NULL,
                last_login TIMESTAMP WITH TIME ZONE,
                is_superuser BOOLEAN NOT NULL,
                username VARCHAR(150) NOT NULL UNIQUE,
                first_name VARCHAR(150) NOT NULL,
                last_name VARCHAR(150) NOT NULL,
                email VARCHAR(254) NOT NULL,
                is_staff BOOLEAN NOT NULL,
                is_active BOOLEAN NOT NULL,
                date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
                position VARCHAR(100),
                phone VARCHAR(20),
                department_id INTEGER
            )
        """)
        print("✅ Таблица users_customuser создана")
    except Exception as e:
        print(f"⚠️ Ошибка при создании таблицы users_customuser: {e}")
    
    # Создаем другие необходимые таблицы
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messenger_department (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                code VARCHAR(10) NOT NULL UNIQUE,
                description TEXT
            )
        """)
        print("✅ Таблица messenger_department создана")
    except Exception as e:
        print(f"⚠️ Ошибка при создании messenger_department: {e}")

print("🛠️  Таблицы проверены/созданы")
