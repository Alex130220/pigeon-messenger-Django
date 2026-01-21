import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.conversation_id = int(self.scope['url_route']['kwargs']['conversation_id'])
            self.room_group_name = f'chat_{self.conversation_id}'
            self.user = self.scope["user"]
            
            if isinstance(self.user, AnonymousUser):
                await self.close(code=4001)
                return

            if not await self.is_participant():
                await self.close(code=4003)
                return

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            # Уведомление о подключении
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'system_message',
                    'message': f'{self.user.username} присоединился к чату',
                    'is_system': True
                }
            )
            
        except KeyError:
            await self.close(code=4000)  # Неверный URL
        except ValueError:
            await self.close(code=4000)  # Нечисловой ID
        except Exception as e:
            print(f"WebSocket error: {e}")
            await self.close(code=4002)  # Другая ошибка

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            # Уведомление об отключении
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'system_message',
                    'message': f'{self.user.username} покинул чату',
                    'is_system': True
                }
            )
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            
            if data.get('type') == 'chat_message':
                # Обработка обычного сообщения
                message = data['message']
                
                # Сохраняем в БД
                message_obj = await self.save_message(message)
                
                # Отправляем участникам
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': self.user.username,
                        'user_id': self.user.id,
                        'timestamp': str(message_obj.timestamp),
                        'is_system': False
                    }
                )
            elif data.get('type') == 'typing':
                # Обработка индикатора печати
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'username': self.user.username,
                        'is_typing': data['is_typing']
                    }
                )

        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': str(e)
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'timestamp': event['timestamp'],
            'is_system': False
        }))

    async def system_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'system',
            'message': event['message'],
            'is_system': True
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username'],
            'is_typing': event['is_typing']
        }))

    @sync_to_async
    def is_participant(self):
        return self.user.conversations.filter(id=self.conversation_id).exists()

    @sync_to_async
    def save_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content
        )
