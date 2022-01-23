import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
from .models import User, Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        account_user_id = text_data_json['account_user_id']
        user_id = text_data_json['user_id']

        account_user = User.objects.get(id=account_user_id)
        user = User.objects.get(id=user_id)
        print(account_user.first_name)
        print(user.first_name)

        # Send message to room group
        # await self.save_message(account_user, user, self.room_name, message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

# @sync_to_async
# def save_message(self, account_user, user, room, message):
#     chat = Chat.objects.create(room_id=room)
#     chat_message = Message.objects.create(content=message, sender=account_user, chat_room=chat)
#     account_user.chatrooms.add(chat)
#     user.chatrooms.add(chat)
