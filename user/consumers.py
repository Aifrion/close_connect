import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import User, Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        account_user_id = text_data_json['account_user_id']
        user_id = text_data_json['user_id']

        await self.save_message(account_user_id, user_id, self.room_name, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def save_message(self, account_user_id, user_id, room, message):
        account_user = User.objects.get(id=account_user_id)
        user = User.objects.get(id=user_id)
        print(Chat.objects.filter(room_id=room))
        if len(Chat.objects.filter(room_id=room)) < 1:
            chat = Chat.objects.create(room_id=room)
            account_user.chatrooms.add(chat)
            user.chatrooms.add(chat)
        else:
            print('running')
            chat = Chat.objects.filter(room_id=room)[0]
        chat_message = Message.objects.create(content=message, sender=account_user, chat_room=chat)

# import json
# from asgiref.sync import async_to_sync, sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import User, Chat, Message
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         print(self.room_name)
#         print(self.room_group_name)
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         account_user_id = text_data_json['account_user_id']
#         user_id = text_data_json['user_id']
#
#         account_user = User.objects.get(id=account_user_id)
#         user = User.objects.get(id=user_id)
#         print(account_user.first_name)
#         print(user.first_name)
#
#         # Send message to room group
#         await self.save_message(account_user, user, self.room_name, message)
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     # Receive message from room group
#
#     async def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
#
#     @sync_to_async
#     def save_message(self, account_user, user, room, message):
#         chat = Chat.objects.create(room_id=room)
#         chat_message = Message.objects.create(content=message, sender=account_user, chat_room=chat)
#         account_user.chatrooms.add(chat)
#         user.chatrooms.add(chat)
