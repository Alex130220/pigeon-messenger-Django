#!/usr/bin/env python
"""
ЭКСТРЕННЫЙ СКРИПТ для создания таблицы users_customuser на Render
"""
import os
import sys
import django
from django.db import connection

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeon.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Ошибка настройки Django: {e}")
    sys.exit(1)

print("🚨 ЭКСТРЕННОЕ СОЗДАНИЕ ТАБЛИЦЫ users_customuser")

# SQL для создания таблицы
sql = """
DO $$
BEGIN
    -- Проверяем существование таблицы
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'users_customuser') THEN
        -- Создаем таблицу
        CREATE TABLE users_customuser (
            id SERIAL PRIMARY KEY,
            password VARCHAR(128) NOT NULL,
            last_login TIMESTAMP WITH TIME ZONE NULL,
            is_superuser BOOLEAN NOT NULL DEFAULT false,
            username VARCHAR(150) UNIQUE NOT NULL,
            first_name VARCHAR(150) NOT NULL DEFAULT '',
            last_name VARCHAR(150) NOT NULL DEFAULT '',
            email VARCHAR(254) NOT NULL DEFAULT '',
            is_staff BOOLEAN NOT NULL DEFAULT false,
            is_active BOOLEAN NOT NULL DEFAULT true,
            date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            avatar VARCHAR(100) NULL,
            phone VARCHAR(20) NULL,
            bio TEXT NULL,
            birth_date DATE NULL,
            position VARCHAR(100) NULL
        );
        
        -- Создаем индексы
        CREATE INDEX users_customuser_username_idx ON users_customuser (username);
        CREATE INDEX users_customuser_email_idx ON users_customuser (email);
        
        RAISE NOTICE '✅ Таблица users_customuser создана успешно';
    ELSE
        RAISE NOTICE 'ℹ️ Таблица users_customuser уже существует';
    END IF;
END
$$;
"""

try:
    with connection.cursor() as cursor:
        # Выполняем SQL
        cursor.execute(sql)
        print("✅ SQL команда выполнена")
        
        # Проверяем создание
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename = 'users_customuser'")
        result = cursor.fetchone()
        
        if result:
            print("✅ Таблица users_customuser существует в базе данных")
            
            # Создаем суперпользователя
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            if not User.objects.filter(username='admin').exists():
                try:
                    User.objects.create_superuser(
                        username='admin',
                        email='admin@example.com',
                        password='admin123'
                    )
                    print("✅ Суперпользователь создан: admin / admin123")
                except Exception as e:
                    print(f"⚠️ Не удалось создать суперпользователя: {e}")
            else:
                print("ℹ️ Суперпользователь уже существует")
        else:
            print("❌ Таблица не была создана")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
