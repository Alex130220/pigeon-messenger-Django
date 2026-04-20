import React, { useState, useEffect, useRef } from 'react';
import { connectToChat, sendMessageViaWebSocket, disconnectFromChat } from 'api/websocket';
import { fetchMessages, sendMessage } from 'api/api';
import './Chat.css';
import { WebSocketMessage } from 'types/chat';

interface Message extends WebSocketMessage {
  // Дополнительные свойства, если нужны
}

const Chat = ({ roomName }: { roomName: string }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loadMessages = async () => {
      try {
        const history = await fetchMessages();
        setMessages(history);
      } catch (error) {
        console.error('Failed to load messages:', error);
      }
    };

    loadMessages();

    connectToChat(
      roomName,
      (msg: WebSocketMessage) => {
        const message: Message = {
          ...msg,
          id: msg.id
        };
        setMessages(prev => [...prev, message]);
      },
      (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      }
    );

    setIsConnected(true);

    return () => {
      disconnectFromChat();
    };
  }, [roomName]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!newMessage.trim()) return;

    try {
      await sendMessage(newMessage);
      sendMessageViaWebSocket(newMessage);
      setNewMessage('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-status">
        Status: {isConnected ? 'Connected' : 'Disconnected'} | Room: {roomName}
      </div>

      <div className="messages-container">
        {messages.map((message, index) => (
          <div 
            key={`${message.id}-${index}`}
            className={`message ${message.type === 'system' ? 'system' : 'user'}`}
          >
            {message.type !== 'system' && (
              <span className="sender">{message.sender}: </span>
            )}
            <span className="content">{message.content}</span>
            <span className="timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </span>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Type a message..."
        />
        <button 
          onClick={handleSendMessage} 
          disabled={!isConnected}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;