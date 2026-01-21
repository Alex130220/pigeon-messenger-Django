#!/usr/bin/env python
"""
Скрипт для создания статических файлов
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def create_static_structure():
    """Создает структуру статических файлов"""
    
    # Создаем директории
    static_dirs = [
        'static/css',
        'static/js',
        'static/images',
        'staticfiles',
        'media',
        'sessions',
    ]
    
    for dir_path in static_dirs:
        dir_full = BASE_DIR / dir_path
        os.makedirs(dir_full, exist_ok=True)
        print(f"✓ Создана директория: {dir_full}")
    
    # Создаем CSS файл
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
    print(f"✓ Создан файл: {css_file}")
    
    # Создаем JS файл
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
    print(f"✓ Создан файл: {js_file}")
    
    # Создаем изображение-заглушку (base64 encoded placeholder)
    img_placeholder = """<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#667eea"/>
        <circle cx="100" cy="70" r="30" fill="white"/>
        <ellipse cx="100" cy="120" rx="50" ry="40" fill="white"/>
        <path d="M60,140 Q100,180 140,140" stroke="#764ba2" stroke-width="3" fill="none"/>
        <text x="100" y="185" text-anchor="middle" fill="white" font-family="Arial" font-size="14">Pigeon</text>
    </svg>"""
    
    # Сохраняем SVG как PNG placeholder
    import base64
    img_file = BASE_DIR / 'static' / 'images' / 'Pigeon.png'
    
    # Просто создаем текстовый файл с информацией (на Render будет заменен реальным изображением)
    with open(img_file, 'w', encoding='utf-8') as f:
        f.write("Это placeholder для изображения Pigeon.png\n")
        f.write("Замените этот файл реальным изображением")
    print(f"✓ Создан файл-заглушка: {img_file}")
    
    # Создаем второй placeholder
    img_screenshot = BASE_DIR / 'static' / 'images' / 'app-screenshot.png'
    with open(img_screenshot, 'w', encoding='utf-8') as f:
        f.write("Это placeholder для скриншота приложения\n")
        f.write("Замените этот файл реальным скриншотом")
    print(f"✓ Создан файл-заглушка: {img_screenshot}")
    
    print("\n✅ Структура статических файлов создана успешно!")
    print("📁 Директории:")
    print("  - static/css/style.css")
    print("  - static/js/main.js")
    print("  - static/images/ (с placeholder файлами)")
    print("\n⚠️  Замените placeholder файлы реальными изображениями")

if __name__ == "__main__":
    create_static_structure()
