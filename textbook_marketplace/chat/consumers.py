# from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async

# from django.shortcuts import get_object_or_404
import json
from typing import Any
# from time import time

# from .models import Chat


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self) -> None:
        # print(self.scope)
        user = self.scope['user']

        self.room_name: str = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name: str = f'chat_{self.room_name}'
        await self.channel_layer.group_add(channel=self.channel_name,
                                           group=self.room_group_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(channel=self.channel_name,
                                               group=self.room_group_name)

    async def receive(self, text_data):
        text_data_json: dict[str: Any] = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message',
             'message': message,
             'sender_id': sender.pk,
             })

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))
