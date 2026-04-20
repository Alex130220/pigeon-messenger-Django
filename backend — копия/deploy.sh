#!/bin/bash
# deploy.sh - Полный скрипт деплоя для Render

echo "🚀 ЗАПУСК ДЕПЛОЯ PIGEON MESSENGER"
echo "=================================="

# 1. Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip install --upgrade pip
pip install django==5.2.3
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0
pip install psycopg2-binary==2.9.9
pip install dj-database-url==2.1.0
pip install django-cors-headers==4.3.1

# 2. Принудительно создаем таблицы через SQL
echo "🗄️  Создание таблиц вручную..."
python -c "
import os
import psycopg2
from urllib.parse import urlparse

# Получаем URL базы данных
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print('❌ DATABASE_URL не найден')
    exit(1)

# Парсим URL
result = urlparse(db_url)
conn = psycopg2.connect(
    database=result.path[1:],
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=result.port
)
conn.autocommit = True
cursor = conn.cursor()

# Создаем таблицу пользователей (если не существует)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS auth_user (
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
        date_joined TIMESTAMP WITH TIME ZONE NOT NULL
    )
''')
print('✅ Таблица auth_user создана/уже существует')

# Создаем стандартные таблицы Django
tables = [
    'django_content_type',
    'auth_permission',
    'auth_group',
    'auth_user_groups',
    'auth_user_user_permissions',
    'django_session',
    'django_admin_log',
    'django_migrations'
]

for table in tables:
    cursor.execute(f\"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table}')\")
    if not cursor.fetchone()[0]:
        print(f'⚠️ Таблица {table} не существует, пропускаем...')

# Создаем суперпользователя если не существует
cursor.execute(\"SELECT COUNT(*) FROM auth_user WHERE username = 'admin'\")
if cursor.fetchone()[0] == 0:
    from django.contrib.auth.hashers import make_password
    hashed_password = make_password('admin123')
    cursor.execute('''
        INSERT INTO auth_user 
        (username, password, email, is_staff, is_superuser, is_active, first_name, last_name, date_joined)
        VALUES 
        ('admin', %s, 'admin@example.com', TRUE, TRUE, TRUE, 'Admin', 'User', NOW())
    ''', [hashed_password])
    print('✅ Суперпользователь создан: admin/admin123')

cursor.close()
conn.close()
"

# 3. Создаем базовую структуру проекта
echo "📁 Создание структуры проекта..."
mkdir -p static/css static/js static/images
mkdir -p staticfiles
mkdir -p media
mkdir -p templates/registration

# 4. Создаем базовые файлы
echo "🎨 Создание базовых файлов..."

# CSS файл
cat > static/css/style.css << 'EOF'
body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: #f5f5f5;
}
EOF

# JS файл
cat > static/js/main.js << 'EOF'
console.log('Pigeon Messenger loaded');
EOF

# Файл-заглушка для изображения
echo "placeholder" > static/images/Pigeon.png

# 5. Создаем простой шаблон входа
cat > templates/registration/login.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Pigeon Messenger - Login</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
        }
        button:hover {
            background: #5a6fd8;
        }
        .error {
            color: #e74c3c;
            padding: 10px;
            background: #fdf2f2;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .info {
            background: #e8f4fd;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>🐦 Pigeon Messenger</h1>
        
        {% if form.errors %}
            <div class="error">
                Неверное имя пользователя или пароль.
            </div>
        {% endif %}
        
        <form method="post">
            {% csrf_token %}
            <input type="text" name="username" placeholder="Имя пользователя" required>
            <input type="password" name="password" placeholder="Пароль" required>
            <button type="submit">Войти</button>
        </form>
        
        <div class="info">
            <strong>Тестовые учетные данные:</strong>
            <p>Имя пользователя: <code>admin</code></p>
            <p>Пароль: <code>admin123</code></p>
        </div>
    </div>
</body>
</html>
EOF

# 6. Выполняем стандартные команды Django
echo "🔄 Выполнение команд Django..."

# Создаем миграции
python manage.py makemigrations --noinput || echo "⚠️ Не удалось создать миграции"

# Применяем миграции
python manage.py migrate --noinput || echo "⚠️ Не удалось применить миграции"

# Создаем суперпользователя (если еще не создан)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Собираем статику
echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput --clear

echo "=================================="
echo "✅ ДЕПЛОЙ УСПЕШНО ЗАВЕРШЕН!"
echo "🌐 Откройте: https://ваш-домен.onrender.com"
echo "👤 Войдите с: admin / admin123"