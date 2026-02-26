import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f'room_{self.room_id}'

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        # Inform all users in the group about the new user joining
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "user_status",
                    "status": "online",
                    "user": self.scope["user"].username,
                },
            )

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "user_status",
                    "status": "offline",
                    "user": self.scope["user"].username,
                },
            )

        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            return

        kind = data.get("kind") or "message"

        if kind == "typing":
            is_typing = bool(data.get("is_typing"))
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "typing",
                    "user": user.username,
                    "is_typing": is_typing,
                },
            )
            return

        # Do not persist messages; just broadcast them to the room.
        message = (data.get("message") or "").strip()
        if not message:
            return

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": user.username,
            },
        )

    async def user_status(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "kind": "status",
                    "status": event["status"],
                    "user": event["user"],
                }
            )
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "kind": "message",
                    "message": event["message"],
                    "sender": event["sender"],
                }
            )
        )

    async def typing(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "kind": "typing",
                    "user": event["user"],
                    "is_typing": event["is_typing"],
                }
            )
        )
