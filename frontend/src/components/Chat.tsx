import React, { useEffect, useState } from 'react';
import { Client } from '@stomp/stompjs';
import { fetchMessages } from "../api/api";
import { sendMessageViaWebSocket } from "../api/websocket";

interface Message {
  content: string;
  sender?: string;
  timestamp?: string;
}

interface ChatProps {
  roomName: string;
}

const Chat: React.FC<ChatProps> = ({ roomName }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Загрузка истории сообщений с обработкой ошибок
    const loadMessages = async () => {
      try {
        const data = await fetchMessages();
        setMessages(data);
      } catch (error) {
        console.error('Ошибка загрузки сообщений:', error);
      }
    };

    loadMessages();

    // WebSocket соединение
    const client = new Client({
      brokerURL: 'ws://localhost:8000/ws/chat/general',
      onConnect: () => {
        setIsConnected(true);
        client.subscribe(`/topic/chat/${roomName}`, (message) => {
          try {
            const newMessage = JSON.parse(message.body);
            setMessages(prev => [...prev, newMessage]);
          } catch (error) {
            console.error('Ошибка обработки сообщения:', error);
          }
        });
      },
      onDisconnect: () => {
        setIsConnected(false);
      },
      debug: (str) => {
        console.log('STOMP debug:', str);
      },
      reconnectDelay: 5000,
      heartbeatIncoming: 4000,
      heartbeatOutgoing: 4000,
    });

    client.activate();

    return () => {
      client.deactivate();
    };
  }, [roomName]);

  const handleSend = () => {
    if (input.trim()) {
      try {
        // Отправляем только сообщение (адаптируйте под ваш API)
        sendMessageViaWebSocket(input);
        setInput('');
      } catch (error) {
        console.error('Ошибка отправки сообщения:', error);
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <h2>Чат комнаты: {roomName}</h2>
      <div className="connection-status">
        Статус: {isConnected ? 'Подключено' : 'Отключено'}
      </div>
      <div className="messages-list">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            {msg.sender && <span className="sender">{msg.sender}: </span>}
            <span className="content">{msg.content}</span>
            {msg.timestamp && <span className="timestamp">{msg.timestamp}</span>}
          </div>
        ))}
      </div>
      <div className="message-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Введите сообщение"
          disabled={!isConnected}
        />
        <button 
          onClick={handleSend}
          disabled={!input.trim() || !isConnected}
        >
          Отправить
        </button>
      </div>
    </div>
  );
};

export default Chat;