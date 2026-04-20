document.addEventListener('DOMContentLoaded', function() {
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