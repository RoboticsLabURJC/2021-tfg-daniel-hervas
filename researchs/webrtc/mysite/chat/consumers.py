import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.shortcuts import render

class ChatConsumer(WebsocketConsumer):
    room_list = {}

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Si la sala no existe, se mete en el diccionario
        if self.room_list.get(self.room_group_name) == None:
            self.room_list[self.room_group_name] = []
        
        # Se comprueba que haya hueco en la sala
        if (len(self.room_list[self.room_group_name]) < 2):
            print('Connected: ', self.channel_name)

            if self.room_list.get(self.room_group_name) == None:
                self.room_list[self.room_group_name] = []
            
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Append user channel name if not in list
            #if self.channel_name not in self.channel_list:
            #    self.channel_list.append(self.channel_name)
            self.room_list[self.room_group_name].append(self.channel_name)
            #print('USERS: ', self.channel_list)
            print('[CHAT] GROUPS LIST: ', self.room_list)
            self.accept()
        else:
            self.accept()
            # Responderle con mensaje de que no es aceptado
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type':'denied'
                }
            )

    def disconnect(self, user_code):
        try:
            # Remove user from list
            #self.channel_list.pop(self.channel_list.index(self.channel_name))
            self.room_list[self.room_group_name].pop(self.room_list[self.room_group_name].index(self.channel_name))
            self.room_list.pop(self.room_group_name)
        except (ValueError, KeyError):
            pass
        # If room is empty, delete it from dict

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
        # elif text_data_json['type'] == 'candidate':
        #     #print('Candidate message received')
        #     # Enviar el mensaje al peer opuesto
        #     for channel in self.room_list[self.room_group_name]:
        #         if (channel != self.channel_name) and (self.scope['url_route']['kwargs']['room_name'] == self.room_name):
        #             async_to_sync(self.channel_layer.send)(
        #                 channel,
        #                 {
        #                     'type': text_data_json['type'],
        #                     'candidate': text_data_json['candidate']
        #                 }
        #             )
        # elif text_data_json['type'] == 'offer':
        #     #print('Offer message received')
        #     # Enviar el mensaje al peer opuesto
        #     for channel in self.room_list[self.room_group_name]:
        #         if (channel != self.channel_name) and (self.scope['url_route']['kwargs']['room_name'] == self.room_name):
        #             async_to_sync(self.channel_layer.send)(
        #                 channel,
        #                 {
        #                     'type': text_data_json['type'],
        #                     'offer': text_data_json['offer']
        #                 }
        #             )
        # elif text_data_json['type'] == 'answer':
        #     #print('Answer message received')
        #     for channel in self.room_list[self.room_group_name]:
        #         if (channel != self.channel_name) and (self.scope['url_route']['kwargs']['room_name'] == self.room_name):
        #             async_to_sync(self.channel_layer.send)(
        #                 channel,
        #                 {
        #                     'type': text_data_json['type'],
        #                     'answer': text_data_json['answer']
        #                 }
        #             )
        # elif text_data_json['type'] == 'check-users':
        #     async_to_sync(self.channel_layer.send)(
        #         self.channel_name,
        #         {
        #             'type':'checkusers',
        #             'users':len(self.room_list[self.room_group_name]) > 1
        #         }
        #     )

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
    # # Send candidate message
    # def candidate(self, event):
    #     self.send(text_data=json.dumps({
    #         'type': event['type'],
    #         'candidate': event['candidate']
    #     }))

    # def offer(self, event):
    #     self.send(text_data=json.dumps({
    #         'type': event['type'],
    #         'offer': event['offer']
    #     }))

    # def answer(self, event):
    #     self.send(text_data=json.dumps({
    #         'type': event['type'],
    #         'answer': event['answer']
    #     }))

    # def denied(self, event):
    #     self.send(text_data=json.dumps({
    #         'type': 'denied'
    #     }))

    # def checkusers(self, event):
    #     self.send(text_data=json.dumps({
    #         'type': event['type'],
    #         'users': event['users']
    #     }))

class StreamConsumer(WebsocketConsumer):
    room_list = {}

    def connect(self):
        print('[STREAM] connectado')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Si la sala no existe, se mete en el diccionario
        if self.room_list.get(self.room_group_name) == None:
            self.room_list[self.room_group_name] = []
        
        # Se comprueba que haya hueco en la sala
        if (len(self.room_list[self.room_group_name]) < 2):
            print('[STREAM] Connected: ', self.channel_name)

            if self.room_list.get(self.room_group_name) == None:
                self.room_list[self.room_group_name] = []
            
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Append user channel name if not in list
            #if self.channel_name not in self.channel_list:
            #    self.channel_list.append(self.channel_name)
            self.room_list[self.room_group_name].append(self.channel_name)
            #print('USERS: ', self.channel_list)
            print('[STREAM] GROUPS LIST: ', self.room_list)
            self.accept()
        else:
            self.accept()
            # Responderle con mensaje de que no es aceptado
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type':'denied'
                }
            )

    def disconnect(self, user_code):
        try:
            # Remove user from list
            #self.channel_list.pop(self.channel_list.index(self.channel_name))
            self.room_list[self.room_group_name].pop(self.room_list[self.room_group_name].index(self.channel_name))
            self.room_list.pop(self.room_group_name)
        except (ValueError, KeyError):
            pass
        # If room is empty, delete it from dict

        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('[NOVNC] WebSocket: ', self.channel_name, '! Content: ', text_data_json)
        
        if text_data_json['type'] == 'candidate':
            print('[NOVNC] Candidate message received')
            # Enviar el mensaje al peer opuesto
            for channel in self.room_list[self.room_group_name]:
                if (channel != self.channel_name) and (self.scope['url_route']['kwargs']['room_name'] == self.room_name):
                    async_to_sync(self.channel_layer.send)(
                        channel,
                        {
                            'type': text_data_json['type'],
                            'candidate': text_data_json['candidate']
                        }
                    )
        elif text_data_json['type'] == 'offer':
            print('[NOVNC] Offer message received')
            # Enviar el mensaje al peer opuesto
            for channel in self.room_list[self.room_group_name]:
                if (channel != self.channel_name) and (self.scope['url_route']['kwargs']['room_name'] == self.room_name):
                    async_to_sync(self.channel_layer.send)(
                        channel,
                        {
                            'type': text_data_json['type'],
                            'offer': text_data_json['offer']
                        }
                    )
        elif text_data_json['type'] == 'answer':
            print('[NOVNC] Answer message received')
            for channel in self.room_list[self.room_group_name]:
                if (channel != self.channel_name) and (self.scope['url_route']['kwargs']['room_name'] == self.room_name):
                    async_to_sync(self.channel_layer.send)(
                        channel,
                        {
                            'type': text_data_json['type'],
                            'answer': text_data_json['answer']
                        }
                    )
        elif text_data_json['type'] == 'check-users':
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type':'checkusers',
                    'users':len(self.room_list[self.room_group_name]) > 1
                }
            )

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

    def denied(self, event):
        self.send(text_data=json.dumps({
            'type': 'denied'
        }))

    def checkusers(self, event):
        self.send(text_data=json.dumps({
            'type': event['type'],
            'users': event['users']
        }))