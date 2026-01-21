// src/api/websocket.ts
import { Client } from "@stomp/stompjs";

let stompClient: Client | null = null;

export const connectToChat = (onMessageReceived: (msg: any) => void) => {
    stompClient = new Client({
         brokerURL: 'ws://localhost:8000/ws/chat/general',
        onConnect: () => {
            stompClient?.subscribe("/topic/messages", (message) => {
                onMessageReceived(JSON.parse(message.body));
            });
        },
    });
    stompClient.activate();
};

export const sendMessageViaWebSocket = (message: string) => {
    stompClient?.publish({
        destination: "/app/chat",
        body: JSON.stringify({ content: message }),
    });
};