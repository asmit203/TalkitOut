import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from asgiref.sync import sync_to_async

class ChatRoomConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_chat(self, msg, sender):
        msg = ChatMessage.objects.create(chatroom_name = self.room_name, sender_username=sender, message_content=msg)
        msg.refresh_from_db()
        return msg
    

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        
        msg = await self.create_chat(message, username)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
                'id_pk': msg.message_id 
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']
        id_pk = event['id_pk']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'id_pk': id_pk
        }))

