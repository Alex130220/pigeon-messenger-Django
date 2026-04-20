# migrate_all.py
import os
import sys
import django
from django.db import connection, transaction

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pigeon.settings')
django.setup()

print("🚀 ЗАПУСК ПОЛНОЙ МИГРАЦИИ БАЗЫ ДАННЫХ")
print("=" * 50)

def create_customuser_table():
    """Создает таблицу users_customuser вручную"""
    print("🛠️  Создание таблицы users_customuser...")
    
    sql = """
    CREATE TABLE IF NOT EXISTS users_customuser (
        id SERIAL PRIMARY KEY,
        password VARCHAR(128) NOT NULL,
        last_login TIMESTAMP WITH TIME ZONE,
        is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
        username VARCHAR(150) NOT NULL UNIQUE,
        first_name VARCHAR(150) NOT NULL DEFAULT '',
        last_name VARCHAR(150) NOT NULL DEFAULT '',
        email VARCHAR(254) NOT NULL DEFAULT '',
        is_staff BOOLEAN NOT NULL DEFAULT FALSE,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        position VARCHAR(100) DEFAULT '',
        phone VARCHAR(20) DEFAULT '',
        department_id INTEGER
    );
    """
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            print("✅ Таблица users_customuser создана/уже существует")
    except Exception as e:
        print(f"❌ Ошибка при создании users_customuser: {e}")

def create_auth_tables():
    """Создает стандартные таблицы Django auth"""
    print("🔑 Создание стандартных таблиц auth...")
    
    tables_sql = [
        # auth_group
        """CREATE TABLE IF NOT EXISTS auth_group (
            id SERIAL PRIMARY KEY,
            name VARCHAR(150) NOT NULL UNIQUE
        );""",
        
        # auth_permission
        """CREATE TABLE IF NOT EXISTS auth_permission (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            content_type_id INTEGER NOT NULL,
            codename VARCHAR(100) NOT NULL
        );""",
        
        # auth_user_groups
        """CREATE TABLE IF NOT EXISTS auth_user_groups (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL
        );""",
        
        # auth_user_user_permissions
        """CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            permission_id INTEGER NOT NULL
        );""",
        
        # django_content_type
        """CREATE TABLE IF NOT EXISTS django_content_type (
            id SERIAL PRIMARY KEY,
            app_label VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL
        );""",
        
        # django_session
        """CREATE TABLE IF NOT EXISTS django_session (
            session_key VARCHAR(40) PRIMARY KEY,
            session_data TEXT NOT NULL,
            expire_date TIMESTAMP WITH TIME ZONE NOT NULL
        );""",
    ]
    
    try:
        with connection.cursor() as cursor:
            for sql in tables_sql:
                cursor.execute(sql)
            print("✅ Стандартные таблицы auth созданы")
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц auth: {e}")

def create_superuser():
    """Создает суперпользователя если не существует"""
    print("👑 Создание суперпользователя...")
    
    try:
        with connection.cursor() as cursor:
            # Проверяем существует ли пользователь admin
            cursor.execute("SELECT COUNT(*) FROM users_customuser WHERE username = 'admin'")
            count = cursor.fetchone()[0]
            
            if count == 0:
                from django.contrib.auth.hashers import make_password
                password = make_password('admin123')
                
                insert_sql = """
                INSERT INTO users_customuser 
                (username, password, email, is_staff, is_superuser, is_active, first_name, last_name, date_joined)
                VALUES 
                ('admin', %s, 'admin@example.com', TRUE, TRUE, TRUE, 'Admin', 'User', CURRENT_TIMESTAMP)
                """
                cursor.execute(insert_sql, [password])
                print("✅ Суперпользователь 'admin' создан (пароль: admin123)")
            else:
                print("✅ Суперпользователь 'admin' уже существует")
    except Exception as e:
        print(f"❌ Ошибка при создании суперпользователя: {e}")

def main():
    """Основная функция миграции"""
    print("🔍 Проверка подключения к базе данных...")
    
    try:
        # Проверяем подключение
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Подключение к базе данных успешно")
    except Exception as e:
        print(f"❌ Не удалось подключиться к базе данных: {e}")
        return
    
    # Создаем таблицы
    create_customuser_table()
    create_auth_tables()
    
    # Создаем суперпользователя
    create_superuser()
    
    print("=" * 50)
    print("✅ ВСЕ МИГРАЦИИ ВЫПОЛНЕНЫ УСПЕШНО!")
    print("🎉 Теперь вы можете войти с логином: admin, пароль: admin123")

if __name__ == "__main__":
    main()
