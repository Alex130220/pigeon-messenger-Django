// Основной JavaScript файл для Pigeon Messenger
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
