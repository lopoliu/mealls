from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync

# 实现群聊功能
# group为房间id


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_send)(group, {"type": 'send.msg', 'message': message})

    def send_msg(self, message):
        text = message['message']['text']
        self.send(text)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer
