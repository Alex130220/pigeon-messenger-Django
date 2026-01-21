#!/usr/bin/env python
"""
Скрипт для создания статических файлов для Pigeon Messenger
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def create_static_files():
    """Создает все необходимые статические файлы"""
    
    print("Создание структуры статических файлов...")
    
    # Создаем директории
    directories = [
        'static/css',
        'static/js',
        'static/images',
        'staticfiles',
        'media',
        'sessions',
    ]
    
    for dir_path in directories:
        dir_full = BASE_DIR / dir_path
        os.makedirs(dir_full, exist_ok=True)
        print(f"✓ Создана директория: {dir_path}")
    
    # Создаем CSS файл
    css_content = """/* Основные стили Pigeon Messenger */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #38a169;
    --danger-color: #e53e3e;
    --warning-color: #d69e2e;
    --light-color: #f7fafc;
    --dark-color: #2d3748;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    min-height: 100vh;
    color: var(--dark-color);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Навигация */
.navbar {
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    padding: 15px 0;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: var(--primary-color);
    font-size: 24px;
    font-weight: bold;
}

.logo img {
    height: 40px;
    margin-right: 10px;
}

.nav-links {
    display: flex;
    gap: 20px;
    align-items: center;
}

/* Кнопки */
.btn {
    padding: 10px 25px;
    background: var(--primary-color);
    color: white;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 16px;
    display: inline-block;
    text-align: center;
}

.btn:hover {
    background: #5a67d8;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
    background: var(--secondary-color);
}

.btn-secondary:hover {
    background: #5a3792;
}

.btn-success {
    background: var(--success-color);
}

.btn-danger {
    background: var(--danger-color);
}

/* Hero секция */
.hero {
    text-align: center;
    padding: 100px 20px;
    color: white;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 20px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero p {
    font-size: 1.2rem;
    max-width: 600px;
    margin: 0 auto 40px;
    line-height: 1.6;
    opacity: 0.9;
}

/* Карточки фич */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    padding: 80px 20px;
}

.feature-card {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-10px);
}

.feature-card h3 {
    color: var(--primary-color);
    margin-bottom: 15px;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.feature-card p {
    color: #666;
    line-height: 1.6;
}

/* Формы */
.form-group {
    margin-bottom: 20px;
}

.form-label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: var(--dark-color);
}

.form-control {
    width: 100%;
    padding: 12px 15px;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    font-size: 16px;
    transition: border-color 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Сообщения и уведомления */
.alert {
    padding: 15px 20px;
    border-radius: 5px;
    margin: 15px 0;
    color: white;
}

.alert-success {
    background: var(--success-color);
}

.alert-error {
    background: var(--danger-color);
}

.alert-info {
    background: var(--primary-color);
}

.alert-warning {
    background: var(--warning-color);
}

/* Сообщения в чате */
.messages-container {
    background: white;
    border-radius: 10px;
    padding: 30px;
    margin: 40px 0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.message {
    padding: 15px;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.message:last-child {
    border-bottom: none;
}

.message-info {
    flex: 1;
}

.message-sender {
    font-weight: bold;
    color: var(--primary-color);
    margin-bottom: 5px;
}

.message-content {
    color: var(--dark-color);
    line-height: 1.5;
}

.message-time {
    color: #888;
    font-size: 0.9rem;
    white-space: nowrap;
    margin-left: 20px;
}

/* Footer */
footer {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 40px 0;
    text-align: center;
    color: white;
    margin-top: 80px;
}

.footer-links {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin: 20px 0;
}

.footer-links a {
    color: white;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer-links a:hover {
    color: #e2e8f0;
    text-decoration: underline;
}

/* Адаптивность */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5rem;
    }
    
    .features {
        grid-template-columns: 1fr;
        padding: 40px 20px;
    }
    
    .nav-links {
        flex-direction: column;
        gap: 10px;
        width: 100%;
    }
    
    .navbar .container {
        flex-direction: column;
        gap: 15px;
    }
    
    .footer-links {
        flex-direction: column;
        gap: 15px;
    }
}

/* Утилиты */
.text-center { text-align: center; }
.mt-1 { margin-top: 10px; }
.mt-2 { margin-top: 20px; }
.mt-3 { margin-top: 30px; }
.mb-1 { margin-bottom: 10px; }
.mb-2 { margin-bottom: 20px; }
.mb-3 { margin-bottom: 30px; }
.p-1 { padding: 10px; }
.p-2 { padding: 20px; }
.p-3 { padding: 30px; }
"""
    
    css_file = BASE_DIR / 'static' / 'css' / 'style.css'
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✓ Создан файл: static/css/style.css")
    
    # Создаем JS файл
    js_content = """// Основной JavaScript файл для Pigeon Messenger

console.log('Pigeon Messenger загружен успешно! 🚀');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM готов');
    
    // Инициализация приложения
    initApp();
    
    // Проверка подключения к API
    checkApiConnection();
    
    // Настройка обработчиков событий
    setupEventListeners();
    
    // Анимации для кнопок
    setupButtonAnimations();
});

function initApp() {
    console.log('Инициализация Pigeon Messenger...');
    
    // Проверка состояния аутентификации
    updateAuthState();
    
    // Инициализация форм
    initForms();
}

function checkApiConnection() {
    console.log('Проверка подключения к API...');
    
    fetch('/health/')
        .then(response => {
            if (response.ok) {
                console.log('✅ API подключен');
                updateConnectionStatus(true);
                showToast('API подключен успешно', 'success');
            } else {
                console.warn('⚠️ API ответил с ошибкой');
                updateConnectionStatus(false);
            }
        })
        .catch(error => {
            console.error('❌ Ошибка подключения к API:', error);
            updateConnectionStatus(false);
            showToast('Не удалось подключиться к серверу', 'error');
        });
}

function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        statusElement.textContent = connected ? 'Подключено' : 'Не подключено';
        statusElement.className = connected ? 'status-connected' : 'status-disconnected';
    }
}

function updateAuthState() {
    const body = document.body;
    const isAuthenticated = body.classList.contains('authenticated');
    
    console.log('Пользователь аутентифицирован:', isAuthenticated);
    
    // Обновляем элементы с data-auth атрибутами
    document.querySelectorAll('[data-auth]').forEach(element => {
        const authType = element.getAttribute('data-auth');
        const shouldShow = (authType === 'authenticated' && isAuthenticated) ||
                          (authType === 'anonymous' && !isAuthenticated);
        
        element.style.display = shouldShow ? '' : 'none';
    });
}

function initForms() {
    console.log('Инициализация форм...');
    
    // Добавляем валидацию форм
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#e53e3e';
                    isValid = false;
                } else {
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showToast('Пожалуйста, заполните все обязательные поля', 'error');
            }
        });
    });
}

function setupEventListeners() {
    console.log('Настройка обработчиков событий...');
    
    // Обработчик для всех ссылок
    document.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            console.log('Нажата ссылка:', this.href);
        });
    });
    
    // Обработчик для логаута
    const logoutForms = document.querySelectorAll('form[action*="logout"]');
    logoutForms.forEach(form => {
        form.addEventListener('submit', function() {
            if (!confirm('Вы уверены, что хотите выйти?')) {
                return false;
            }
        });
    });
}

function setupButtonAnimations() {
    // Анимация нажатия для кнопок
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('mouseup', function() {
            this.style.transform = '';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// Вспомогательные функции
function showToast(message, type = 'info') {
    console.log(`Toast [${type}]: ${message}`);
    
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${getToastColor(type)};
        color: white;
        border-radius: 5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: toastSlideIn 0.3s ease;
        max-width: 400px;
        word-break: break-word;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toastSlideOut 0.3s ease';
        setTimeout(() => {
            if (toast.parentNode) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

function getToastColor(type) {
    const colors = {
        'success': '#38a169',
        'error': '#e53e3e',
        'warning': '#d69e2e',
        'info': '#3182ce'
    };
    return colors[type] || colors.info;
}

// Добавляем стили для анимаций
const style = document.createElement('style');
style.textContent = `
    @keyframes toastSlideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes toastSlideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .status-connected {
        color: #38a169;
        font-weight: bold;
    }
    
    .status-disconnected {
        color: #e53e3e;
        font-weight: bold;
    }
    
    .toast-success { background: #38a169; }
    .toast-error { background: #e53e3e; }
    .toast-warning { background: #d69e2e; }
    .toast-info { background: #3182ce; }
`;
document.head.appendChild(style);

// Экспортируем функции для использования в других скриптах
window.PigeonMessenger = {
    showToast,
    checkApiConnection,
    updateAuthState
};
"""
    
    js_file = BASE_DIR / 'static' / 'js' / 'main.js'
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✓ Создан файл: static/js/main.js")
    
    # Создаем placeholder изображения
    # SVG placeholder для Pigeon.png
    svg_pigeon = """<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#667eea"/>
        <circle cx="100" cy="80" r="40" fill="white" opacity="0.9"/>
        <path d="M60,120 Q100,160 140,120" stroke="#764ba2" stroke-width="4" fill="none"/>
        <circle cx="80" cy="70" r="8" fill="#764ba2"/>
        <circle cx="120" cy="70" r="8" fill="#764ba2"/>
        <path d="M90,95 Q100,110 110,95" stroke="#764ba2" stroke-width="2" fill="none"/>
        <text x="100" y="185" text-anchor="middle" fill="white" font-family="Arial" font-size="16" font-weight="bold">PIGEON</text>
    </svg>"""
    
    pigeon_file = BASE_DIR / 'static' / 'images' / 'Pigeon.svg'
    with open(pigeon_file, 'w', encoding='utf-8') as f:
        f.write(svg_pigeon)
    print(f"✓ Создан файл: static/images/Pigeon.svg")
    
    # Создаем PNG placeholder (текстовый файл с информацией)
    pigeon_png_file = BASE_DIR / 'static' / 'images' / 'Pigeon.png'
    with open(pigeon_png_file, 'w', encoding='utf-8') as f:
        f.write("Placeholder для Pigeon.png\n")
        f.write("Замените этот файл реальным изображением логотипа\n")
        f.write("Рекомендуемый размер: 200x200 пикселей")
    print(f"✓ Создан файл-заглушка: static/images/Pigeon.png")
    
    # Создаем placeholder для скриншота
    screenshot_file = BASE_DIR / 'static' / 'images' / 'app-screenshot.png'
    with open(screenshot_file, 'w', encoding='utf-8') as f:
        f.write("Placeholder для app-screenshot.png\n")
        f.write("Замените этот файл реальным скриншотом приложения\n")
        f.write("Рекомендуемый размер: 800x400 пикселей")
    print(f"✓ Создан файл-заглушка: static/images/app-screenshot.png")
    
    print("\n" + "="*50)
    print("✅ Структура статических файлов создана успешно!")
    print("="*50)
    print("\n📁 Созданные файлы:")
    print("  - static/css/style.css - Основные стили")
    print("  - static/js/main.js - JavaScript логика")
    print("  - static/images/Pigeon.svg - SVG логотип")
    print("  - static/images/Pigeon.png - Placeholder для PNG логотипа")
    print("  - static/images/app-screenshot.png - Placeholder для скриншота")
    print("\n⚠️  Рекомендации:")
    print("  1. Замените placeholder файлы реальными изображениями")
    print("  2. Для Pigeon.png используйте PNG с прозрачным фоном")
    print("  3. Размер логотипа: 200x200 пикселей")
    print("  4. Размер скриншота: 800x400 пикселей")
    print("\n🚀 Для применения изменений выполните:")
    print("  python manage.py collectstatic")
    print("="*50)

if __name__ == "__main__":
    create_static_files()
