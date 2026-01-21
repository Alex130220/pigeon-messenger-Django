import { Client } from "@stomp/stompjs";
import { WebSocketMessage } from 'types/chat';

let stompClient: Client | null = null;

export const connectToChat = (
  roomName: string,
  onMessageReceived: (msg: WebSocketMessage) => void,
  onError?: (error: string) => void
) => {
  stompClient = new Client({
    brokerURL: `ws://localhost:8000/ws/chat/${roomName}/`,
    reconnectDelay: 5000,
    heartbeatIncoming: 4000,
    heartbeatOutgoing: 4000,
    onConnect: () => {
      stompClient?.subscribe(`/topic/chat/${roomName}`, (message) => {
        try {
          const parsedMessage: WebSocketMessage = JSON.parse(message.body);
          onMessageReceived(parsedMessage);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
          onError?.('Invalid message format');
        }
      });
    },
    onStompError: (frame) => {
      onError?.(frame.headers.message || 'Unknown STOMP error');
    },
    onWebSocketError: (error) => {
      console.error('WebSocket connection error:', error);
      onError?.('WebSocket connection failed');
    }
  });

  stompClient.activate();
};

export const sendMessageViaWebSocket = (content: string) => {
  if (!stompClient?.connected) {
    console.error('Cannot send message - WebSocket not connected');
    return;
  }

  const message: WebSocketMessage = {
    content,
    sender: 'currentUser', // Замените на реального отправителя
    timestamp: new Date().toISOString(),
    type: 'user',
    id: Date.now().toString()
  };

  stompClient.publish({
    destination: `/app/chat`,
    body: JSON.stringify(message),
    headers: {
      'content-type': 'application/json'
    }
  });
};

export const disconnectFromChat = () => {
  if (stompClient?.connected) {
    stompClient.deactivate();
  }
  stompClient = null;
};