import json

from channels.db import database_sync_to_async
from channels.consumer import  AsyncConsumer

from channels.exceptions import StopConsumer

from chat.models.chat import Thread, Message
from user.models.friend import Friend

class ChatConsumer(AsyncConsumer):
    def __init__(self, *args, **kwargs):
        self.connected = False

    async def websocket_connect(self, event):
        user1 = self.scope['user']
        user2 = self.scope['url_route']['kwargs']['name']
        
        are_friends = await self.are_friends(user1.username, user2)
        
        if are_friends:
            thread = await self.get_thread(user1, user2)
            self.thread = thread
            
            chat_room =  f"chat_{thread.id}"
            self.chat_room = chat_room
            await self.channel_layer.group_add(
                self.chat_room,
                self.channel_name
            )

            self.connected = True
            await self.send({   
                "type": "websocket.accept"
            })

        else:
            await self.send({
                "type": "websocket.disconnect",
            })

    async def websocket_receive(self, event):
        json_data = event.get('text')
        if json_data is not None:
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
        if self.connected:
            await self.channel_layer.group_discard(
                self.chat_room,
                self.channel_name 
            )
            self.connected = False

        raise StopConsumer()

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def create_chat_message(self,me, msg):
        thread = self.thread
        return Message.objects.create(thread=thread, user=me, message=msg)

    @database_sync_to_async
    def are_friends(self, user1, user2):
        return Friend.objects.are_friends(user1, user2)
        