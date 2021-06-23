import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    channel_list = []

    def connect(self):
        if len(self.channel_list) < 2:
            print('Connected: ', self.channel_name)
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Append user channel name if not in list
            if self.channel_name not in self.channel_list:
                self.channel_list.append(self.channel_name)
            print('USERS: ', self.channel_list)
            self.accept()
        else:
            # Responderle con mensaje de que no es aceptado
            pass

    def disconnect(self, user_code):
        # Remove user from list
        self.channel_list.pop(self.channel_list.index(self.channel_name))

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #print('WebSocket received from: ', self.scope['user'], '! Content: ', text_data_json)
        
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
            print('Candidate message received')
            # Enviar el mensaje al peer opuesto
            for channel in self.channel_list:
                if channel != self.channel_name:
                    async_to_sync(self.channel_layer.send)(
                        channel,
                        {
                            'type': text_data_json['type'],
                            'candidate': text_data_json['candidate']
                        }
                    )
        elif text_data_json['type'] == 'offer':
            print('Offer message received')
            # Enviar el mensaje al peer opuesto
            for channel in self.channel_list:
                if channel != self.channel_name:
                    async_to_sync(self.channel_layer.send)(
                        channel,
                        {
                            'type': text_data_json['type'],
                            'offer': text_data_json['offer']
                        }
                    )
        elif text_data_json['type'] == 'answer':
            print('Answer message received')
            for channel in self.channel_list:
                if channel != self.channel_name:
                    async_to_sync(self.channel_layer.send)(
                        channel,
                        {
                            'type': text_data_json['type'],
                            'answer': text_data_json['answer']
                        }
                    )


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
    # Send candidate message
    def candidate(self, event):
        self.send(text_data=json.dumps({
            'type': event['type'],
            'candidate': event['candidate']
        }))

    def offer(self, event):
        self.send(text_data=json.dumps({
            'type': event['type'],
            'offer': event['offer']
        }))

    def answer(self, event):
        self.send(text_data=json.dumps({
            'type': event['type'],
            'answer': event['answer']
        }))