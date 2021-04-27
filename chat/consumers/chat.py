import json

from channels.db import database_sync_to_async
from channels.consumer import  AsyncConsumer

from chat.models.chat import Thread, Message

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        user1 = self.scope['user']
        user2 = self.scope['url_route']['kwargs']['name']
        
        thread = await self.get_thread(user1, user2)
        self.thread = thread
        
        chat_room =  f"chat_{thread.id}"
        self.chat_room = chat_room

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({   
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        json_data = event.get('text')
        if data is not None:
            dict_data = json.loads(json_data)
            msg = dict_data.get('message')

            user = self.scope['user']
            username = user.username

            res = {
                'message': msg,
                'username': username
            }

            await self.create_chat_message(user, msg)
            
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(res)
                }
            )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name 
        )

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self,me, msg):
        thread_obj = self.thread_obj
        return Message.objects.create(thread=thread_obj, user=me, message=msg)