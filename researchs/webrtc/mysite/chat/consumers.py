import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    tokens_list = []

    def connect(self):
        print('Connected: ', self.channel_name)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Append user channel name
        self.tokens_list.append(self.channel_name)

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
        print('WebSocket received from: ', self.scope['user'], '! Content: ', text_data_json)
        
        # Send message to room group
        if text_data_json['type'] == 'chat_message':
            message = text_data_json['message']
            token = text_data_json['token']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'token':token,
                    'message': message
                }
            )
        elif text_data_json['type'] == 'candidate':
            print('New candidate')

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        token = event['token']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'chat_message',
            'token':token,
            'message': message
        }))