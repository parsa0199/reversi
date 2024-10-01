# game/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.room_group_name = f'game_{self.game_id}'

        # Join game group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave game group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        player = data['player']
        move = data['move']

        # Handle game logic, update board, etc.
        # You can add the logic to check moves and update the board here.

        # Broadcast move to all players in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_move',
                'action': action,
                'player': player,
                'move': move,
            }
        )

    # Receive message from group
    async def game_move(self, event):
        action = event['action']
        player = event['player']
        move = event['move']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': action,
            'player': player,
            'move': move
        }))
