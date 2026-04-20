export interface WebSocketMessage {
  id: string; // Измените на обязательное поле
  content: string;
  sender: string;
  timestamp: string;
  type?: 'user' | 'system';
}

export type Message = WebSocketMessage; // Алиас для совместимости