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
    
    # Создаем CSS файл (style.css)
    css_content = """/* Основные стили Pigeon Messenger */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
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
    color: #667eea;
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
}

.btn {
    padding: 10px 25px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 16px;
}

.btn:hover {
    background: #5a67d8;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
    background: #718096;
}

.btn-secondary:hover {
    background: #4a5568;
}

/* Основной контент */
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
}

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
    color: #667eea;
    margin-bottom: 15px;
    font-size: 1.5rem;
}

.feature-card p {
    color: #666;
    line-height: 1.6;
}

/* Сообщения */
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
    align-items: center;
}

.message:last-child {
    border-bottom: none;
}

.message-info {
    flex: 1;
}

.message-sender {
    font-weight: bold;
    color: #667eea;
}

.message-content {
    color: #333;
    margin-top: 5px;
}

.message-time {
    color: #888;
    font-size: 0.9rem;
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
}

/* Уведомления */
.notification {
    padding: 15px 20px;
    border-radius: 5px;
    margin: 10px 0;
    color: white;
}

.notification-success {
    background: #38a169;
}

.notification-error {
    background: #e53e3e;
}

.notification-info {
    background: #3182ce;
}

/* Адаптивность */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5rem;
    }
    
    .features {
        grid-template-columns: 1fr;
    }
    
    .nav-links {
        flex-direction: column;
        gap: 10px;
    }
}
"""
    
    css_file = BASE_DIR / 'static' / 'css' / 'style.css'
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✓ Создан файл: static/css/style.css")
    
    # Создаем кастомный CSS файл (custom.css)
    custom_css_content = """/* Кастомный скроллбар */
.chat-messages::-webkit-scrollbar {
    width: 8px;
}

.chat-messages::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 10px;
}

/* Анимация набора сообщения */
.typing-indicator {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}
"""
    
    custom_css_file = BASE_DIR / 'static' / 'css' / 'custom.css'
    with open(custom_css_file, 'w', encoding='utf-8') as f:
        f.write(custom_css_content)
    print(f"✓ Создан файл: static/css/custom.css")
    
    # Создаем основной JS файл (main.js)
    js_content = """// Основной JavaScript файл для Pigeon Messenger
console.log('Pigeon Messenger загружен');

document.addEventListener('DOMContentLoaded', function() {
    // Проверка подключения к API
    checkApiConnection();
    
    // Обработчики событий
    setupEventListeners();
});

function checkApiConnection() {
    fetch('/health/')
        .then(response => {
            if (response.ok) {
                updateConnectionStatus(true);
            } else {
                updateConnectionStatus(false);
            }
        })
        .catch(() => {
            updateConnectionStatus(false);
        });
}

function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    if (statusElement) {
        statusElement.textContent = connected ? 'Подключено' : 'Не подключено';
        statusElement.className = connected ? 'status-connected' : 'status-disconnected';
    }
}

function setupEventListeners() {
    // Обработчики кнопок
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
}

// Стили для статуса подключения
const style = document.createElement('style');
style.textContent = `
    .status-connected {
        color: #38a169;
        font-weight: bold;
    }
    
    .status-disconnected {
        color: #e53e3e;
        font-weight: bold;
    }
`;
document.head.appendChild(style);
"""
    
    js_file = BASE_DIR / 'static' / 'js' / 'main.js'
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✓ Создан файл: static/js/main.js")
    
    # Создаем чат JS файл (chat.js)
    chat_js_content = """document.addEventListener('DOMContentLoaded', function() {
    // Инициализация эмодзи-пикера
    new EmojiPicker({
        trigger: '.emoji-trigger',
        container: '.chat-input',
        input: 'input[name="message"]'
    });

    // Загрузка предыдущих сообщений
    loadPreviousMessages();
});

async function loadPreviousMessages() {
    const response = await fetch('/api/messages/');
    const messages = await response.json();
    messages.forEach(appendMessage);
}
"""
    
    chat_js_file = BASE_DIR / 'static' / 'js' / 'chat.js'
    with open(chat_js_file, 'w', encoding='utf-8') as f:
        f.write(chat_js_content)
    print(f"✓ Создан файл: static/js/chat.js")
    
    # Создаем SVG логотип
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
    
    # Создаем PNG placeholder (информационный файл)
    pigeon_png_file = BASE_DIR / 'static' / 'images' / 'Pigeon.png'
    with open(pigeon_png_file, 'w', encoding='utf-8') as f:
        f.write("Placeholder для Pigeon.png\\n")
        f.write("Замените этот файл реальным изображением логотипа\\n")
        f.write("Рекомендуемый размер: 200x200 пикселей")
    print(f"✓ Создан файл-заглушка: static/images/Pigeon.png")
    
    # Создаем placeholder для скриншота
    screenshot_file = BASE_DIR / 'static' / 'images' / 'app-screenshot.png'
    with open(screenshot_file, 'w', encoding='utf-8') as f:
        f.write("Placeholder для app-screenshot.png\\n")
        f.write("Замените этот файл реальным скриншотом приложения\\n")
        f.write("Рекомендуемый размер: 800x400 пикселей")
    print(f"✓ Создан файл-заглушка: static/images/app-screenshot.png")
    
    # Создаем favicon.ico placeholder
    favicon_file = BASE_DIR / 'static' / 'favicon.ico'
    with open(favicon_file, 'w', encoding='utf-8') as f:
        f.write("Placeholder для favicon.ico\\n")
        f.write("Замените этот файл реальной иконкой сайта")
    print(f"✓ Создан файл-заглушка: static/favicon.ico")
    
    print("\\n" + "="*50)
    print("✅ Структура статических файлов создана успешно!")
    print("="*50)
    print("\\n📁 Созданные файлы:")
    print("  - static/css/style.css - Основные стили")
    print("  - static/css/custom.css - Дополнительные стили")
    print("  - static/js/main.js - Основной JavaScript")
    print("  - static/js/chat.js - JavaScript для чата")
    print("  - static/images/Pigeon.svg - SVG логотип")
    print("  - static/images/Pigeon.png - Placeholder для PNG логотипа")
    print("  - static/images/app-screenshot.png - Placeholder для скриншота")
    print("  - static/favicon.ico - Placeholder для фавиконки")
    print("\\n⚠️  Рекомендации:")
    print("  1. Замените placeholder файлы реальными изображениями")
    print("  2. Для Pigeon.png используйте PNG с прозрачным фоном")
    print("  3. Размер логотипа: 200x200 пикселей")
    print("  4. Размер скриншота: 800x400 пикселей")
    print("\\n🚀 Для применения изменений выполните:")
    print("  python manage.py collectstatic")
    print("="*50)

if __name__ == "__main__":
    create_static_files()
