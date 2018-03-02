from django.conf import settings
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
import random
from .exceptions import ClientError
from theroom.utils import *
from theroom.models import *
import time

# remove old connections
Session.objects.all().delete()
ROOMS = ["waiting_room"]
counter = 0
class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This chat consumer handles websocket connections for chat clients.

    It uses AsyncJsonWebsocketConsumer, which means all the handling functions
    must be async functions, and any sync work (like ORM access) has to be
    behind database_sync_to_async or sync_to_async. For more, read
    http://channels.readthedocs.io/en/latest/topics/consumers.html
    """
    ##### WebSocket event handlers


    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        self.scope["session"]["seed"] = random.randint(1, 1000)

        await self.accept()

        self.scope["session"].save()
        # add to group 0
        await self.join_room('waiting_room')
        # Store which rooms the user has joined on this connection
        self.room = "waiting_room"
        await self.send_place_in_line()

    async def send_place_in_line(self):
        session_key = await get_or_create_session(self.scope)
        place_in_line = await get_place_in_line(session_key)
        await self.send_json({
            'place_in_line': place_in_line,
            'session_key': session_key
        })

    async def boot_bot(self):
        await remove_next_bot_session()
        # await self.chat_leave()
        await self.send_place_in_line()

    async def receive_json(self, content, **kwargs):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        command = content.get("command", None)
        print("receive_json >>>>> getting command", content)

        try:
            if command == "join":
                # Make them join the room
                await self.join_room(content["room"])
            elif command == "leave":
                # Leave the room
                await self.leave_room(content["room"])
            elif command == "send":
                await self.send_room(content["room"], content["message"])
            elif command == "boot_bot":
                print('getting boot_bot command')
                await self.boot_bot()
            elif command == "enter_the_site":
                await self.enter_the_site()
        except ClientError as e:
            # Catch any errors and send it back
            await self.send_json({"error": e.code})

    async def enter_the_site(self):
        session = await get_or_create_session(self.scope)
        place_in_line = await get_place_in_line(session)
        print("enter_the_site", place_in_line)
        if place_in_line == 0:
            print("LUCKY YOU::::::::::>>>>>", session)
            await self.join_room('the_site')
            # url = settings.BASE_URL + 'the_website/'

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        session_key = self.scope['session'].session_key
        print('disconnecting, removing session key', session_key)
        # remove_session(session_key)
        time.sleep(2)
        await self.leave_room('waiting_room')

    ##### Command helper methods called by receive_json
    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """

        # The logged-in user is in our scope thanks to the authentication ASGI middleware

        session = await get_or_create_session(self.scope)
        if room_id == 'the_site':
            print('BACKEND< MARKING FOR ENTERANCE ')
            await update_session_in_room(session)

        # Send a join message if it's turned on
        # lock room down, no one else is allowed to join

        print('join_room', session, room_id)
        await self.channel_layer.group_send(
            room_id,
            {
                "type": "chat.join",
                "room_id": room_id,
                "username":  session,
            }
        )
        # # Store that we're in the room
        self.room = room_id
        # Add them to the group so they get room messages
        await self.channel_layer.group_add(
            self.room,
            self.channel_name,
        )

    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        # room = await get_room_or_error(room_id)
        # Send a leave message if it's turned on

        await self.channel_layer.group_send(
            room_id,
            {
                "type": "chat.leave",
                "room_id": room_id,
            }
        )
        # Remove that we're in the room
        self.room = "0"
        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room_id,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": room_id,
        })

    async def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        # Check they are in this room
        if self.room != room_id:
            raise ClientError("ROOM_ACCESS_DENIED")
        # Get the room and send to the group about it
        session = await get_or_create_session(self.scope)

        # room = await get_room_or_error(room_id)
        await self.channel_layer.group_send(
            room_id,
            {
                "type": "chat.message",
                "room_id": room_id,
                "username": session,
                "message": message,
            }
        )

    ##### Handlers for messages sent over the channel layer

    # These helper methods are named by the types we send - so chat.join becomes chat_join
    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        # add_waiting_member(event["username"])
        session = await get_or_create_session(self.scope)
        await self.send_json(
            {
                "msg_type": settings.MSG_TYPE_ENTER,
                "room": event["room_id"],
                "username": session,
            },
        )

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        session = await get_or_create_session(self.scope)
        await self.send_place_in_line()

        place_in_line = get_place_in_line(session)
        # if place_in_line == 0:
        #     print("LUCKY YOU session::::", session)
        #     # import ipdb; ipdb.set_trace()
        #     await self.join_room('the_site')
        # requests.get('/the_website/', params={'is_allowed':True})

#
#
#     async def chat_message(self, event):
#         """
#         Called when someone has messaged our chat.
#         """
#         # Send a message down to the client
#         session = await get_or_create_session(self.scope)
#
#         await self.send_json(
#             {
#                 "msg_type": settings.MSG_TYPE_MESSAGE,
#                 "room": event["room_id"],
#                 "username": event['username'],
#                 "message": event['message'],
#             },
#         )
#
#         # if event["username"] == await get_or_create_session(self.scope):
#         #     message = Message.objects.create(
#         #         session_id=event["username"],
#         #         message=event["message"])
#         #     message.save()
# #
# # class Bot(ChatConsumer):
# #     def __init__(self):
# #         print("hello world, I am Bot")
# #
