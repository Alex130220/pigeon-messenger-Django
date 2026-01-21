import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';

const Chat = ({ currentUser }) => { // Добавьте currentUser в пропсы
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectWebSocket = () => {
    setConnectionStatus('connecting');
    const socket = new WebSocket(
      `ws://${window.location.host}/ws/chat/general/`
    );

    socket.onopen = () => {
      setIsConnected(true);
      setConnectionStatus('connected');
      addSystemMessage('Вы подключены к чату');
    };

    socket.onclose = () => {
      setIsConnected(false);
      setConnectionStatus('disconnected');
      addSystemMessage('Соединение закрыто. Попытка переподключения...');
      setTimeout(connectWebSocket, 5000); // Автопереподключение через 5 сек
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
      addSystemMessage('Ошибка соединения');
    };

    socket.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.type === 'message') {
          addMessage(data);
        } else if (data.type === 'system') {
          addSystemMessage(data.message);
        }
      } catch (err) {
        console.error('Error parsing message:', err);
      }
    };

    socketRef.current = socket;
  };

  const addMessage = (msg) => {
    setMessages(prev => [...prev, {
      ...msg,
      isOwn: msg.user_id === currentUser?.id // Безопасная проверка
    }]);
  };

  const addSystemMessage = (text) => {
    setMessages(prev => [...prev, {
      message: text,
      isSystem: true,
      timestamp: new Date().toISOString()
    }]);
  };

  const sendMessage = () => {
    if (!message.trim() || !socketRef.current || !isConnected) return;
    
    try {
      socketRef.current.send(JSON.stringify({
        message: message.trim(),
        user_id: currentUser?.id // Добавляем ID пользователя
      }));
      setMessage('');
    } catch (err) {
      console.error('Error sending message:', err);
      addSystemMessage('Ошибка отправки сообщения');
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const getStatusColor = () => {
    switch(connectionStatus) {
      case 'connected': return '#4CAF50';
      case 'connecting': return '#FFC107';
      case 'disconnected': 
      case 'error': 
      default: return '#F44336';
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>Pigeon чат</h2>
        <div className="status-indicator">
          Статус: <span style={{ color: getStatusColor() }}>
            {connectionStatus === 'connected' ? 'Online' : 
             connectionStatus === 'connecting' ? 'Подключение...' : 'Offline'}
          </span>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.isSystem ? 'system' : msg.isOwn ? 'own' : 'other'}`}>
            {!msg.isSystem && (
              <div className="message-header">
                <span className="username">{msg.username || 'Аноним'}</span>
                <span className="timestamp">
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </span>
              </div>
            )}
            <div className="message-content">{msg.message}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Введите сообщение..."
          disabled={!isConnected}
        />
        <button 
          onClick={sendMessage} 
          disabled={!isConnected || !message.trim()}
        >
          Отправить
        </button>
      </div>
    </div>
  );
};

export default Chat;