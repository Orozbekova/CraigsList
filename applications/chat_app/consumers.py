import json

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import AsyncToSync
from channels.db import database_sync_to_async

from .models import Group, Chat


class SyncView(SyncConsumer):
    def websocket_connect(self, event):
        print("connected", event)
        print("channel layer ", self.channel_layer)
        print("channel name", self.channel_name)
        # add channel/user to new or existing group
        AsyncToSync(self.channel_layer.group_add)("friends", self.channel_name)
        self.send({
            'type': 'websocket.accept',
        })

    def websocket_receive(self, event):
        print("messaged received ", event)
        msg = json.loads(event['text'])
        print(msg['msg'])
        group = Group.objects.get(name="friends")
        chat = Chat.objects.create(content=msg['msg'], group=group)
        print(chat)
        AsyncToSync(self.channel_layer.group_send)('friends',
                                                   {
                                                       'type': 'chat.message',
                                                       'message': event['text']
                                                   }
                                                   )
        # self.send({
        #     'type': 'websocket.send',
        #     'text': "yes i received your message.. thank you"
        # })

    def chat_message(self, event):
        print('chat_message:', event)
        self.send(
            {
                'type': 'websocket.send',
                'text': event['message']
            }
        )

    def websocket_disconnect(self, event):
        print("connection closed", event)
        print("disconnected channel_layer ", self.channel_layer)
        print("disconnected channel_name ", self.channel_name)
        AsyncToSync(self.channel_layer.group_discard)('friends', self.channel_name)
        raise StopConsumer()
