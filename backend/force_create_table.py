#!/usr/bin/env python
"""
СКРИПТ ПРИНУДИТЕЛЬНОГО СОЗДАНИЯ ТАБЛИЦЫ users_customuser
"""
import os
import sys
import django
from django.db import connection
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def main():
    print("=" * 70)
    print("🚨 ПРИНУДИТЕЛЬНОЕ СОЗДАНИЕ ТАБЛИЦЫ users_customuser")
    print("=" * 70)
    
    # Настройка Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeon.settings')
    
    try:
        django.setup()
        print("✅ Django настроен")
    except Exception as e:
        print(f"❌ Ошибка настройки Django: {e}")
        return False
    
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
    END $$;
    """
    
    try:
        with connection.cursor() as cursor:
            print("🛠️  Выполняем SQL команду...")
            cursor.execute(sql)
            print("✅ SQL команда выполнена")
            
            # Проверяем создание
            print("🔍 Проверяем создание таблицы...")
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename = 'users_customuser'")
            result = cursor.fetchone()
            
            if result:
                print(f"✅ Таблица существует: {result[0]}")
                
                # Создаем суперпользователя
                print("👑 Создаем суперпользователя...")
                from django.contrib.auth import get_user_model
                User = get_user_model()
                
                try:
                    if not User.objects.filter(username='admin').exists():
                        # Создаем хэш пароля вручную
                        from django.contrib.auth.hashers import make_password
                        admin_user = User.objects.create(
                            username='admin',
                            email='admin@example.com',
                            password=make_password('admin123'),
                            is_superuser=True,
                            is_staff=True,
                            is_active=True
                        )
                        print("✅ Суперпользователь создан: admin / admin123")
                    else:
                        print("ℹ️ Суперпользователь уже существует")
                        
                except Exception as e:
                    print(f"⚠️ Ошибка при создании пользователя: {e}")
                    # Попробуем через SQL
                    try:
                        cursor.execute("""
                            INSERT INTO users_customuser 
                            (username, email, password, is_superuser, is_staff, is_active, date_joined)
                            VALUES 
                            ('admin', 'admin@example.com', 'pbkdf2_sha256$600000$xyz123$...', true, true, true, NOW())
                            ON CONFLICT (username) DO NOTHING;
                        """)
                        print("✅ Пользователь создан через SQL")
                    except Exception as sql_e:
                        print(f"❌ Ошибка SQL: {sql_e}")
            else:
                print("❌ Таблица не была создана")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 70)
    if success:
        print("✅ СКРИПТ ВЫПОЛНЕН УСПЕШНО")
    else:
        print("❌ СКРИПТ ЗАВЕРШИЛСЯ С ОШИБКОЙ")
    print("=" * 70)
    sys.exit(0 if success else 1)
