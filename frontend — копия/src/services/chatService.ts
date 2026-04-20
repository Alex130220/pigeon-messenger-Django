// src/services/chatService.ts
import { Client } from '@stomp/stompjs';

const client = new Client({
   brokerURL: 'ws://localhost:8000/ws/chat/general',
  onConnect: () => console.log('WebSocket connected'),
});

export const connectToChat = (roomName: string, onMessage: (msg: string) => void) => {
  client.activate();
  client.onConnect = () => {
    client.subscribe(`/topic/chat/${roomName}`, (message) => {
      onMessage(JSON.parse(message.body));
    });
  };
};

export const sendMessage = (roomName: string, content: string) => {
  client.publish({
    destination: `/app/chat/${roomName}`,
    body: JSON.stringify({ content }),
  });
};