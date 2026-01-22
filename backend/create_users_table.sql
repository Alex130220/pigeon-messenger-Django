-- Скрипт для создания таблицы users_customuser
CREATE TABLE IF NOT EXISTS users_customuser (
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
CREATE INDEX IF NOT EXISTS users_customuser_username_idx ON users_customuser (username);
CREATE INDEX IF NOT EXISTS users_customuser_email_idx ON users_customuser (email);