import random
import uuid
from channels.db import database_sync_to_async

from .exceptions import ClientError
from theroom.models import *


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_room_or_error(room_id):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    # if not user.is_authenticated:
    #     raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    try:
        room = TheRoom.objects.get(pk=room_id)
        # if room.in_use:
        #     raise ClientError("please wait")
    except TheRoom.DoesNotExist:
        raise ClientError("ROOM_INVALID")
    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    return room

@database_sync_to_async
def get_current_queue():
    # refresh from db
    queue = list(Session.objects.all().order_by('created_at').filter(is_active=True).values_list('key', flat=True))
    print("current queue>>>>>>>>>>>>>>:", queue)
    return queue


def create_bot_session():
    rand_str = 'bot_session_'+ str(uuid.uuid1())
    session = Session.objects.create(key=rand_str, is_active=True)


def create_bot_sessions():
    randint = random.randint(1, 3)
    while randint > 0:
        create_bot_session()
        randint -= 1

@database_sync_to_async
def get_or_create_session(scope):
    current_queue = list(Session.objects.all().order_by('created_at').filter(is_active=True).values_list('key', flat=True))
    # current_queue = get_current_queue()
    print("length of current queue:", len(current_queue))
    if len(current_queue) == 0:
        create_bot_sessions()

    session_key = scope['session'].session_key
    session, created = Session.objects.get_or_create(key=session_key)
    if created:
        print('session created:', session)
    session.is_active = True
    session.save()
    return session.key

@database_sync_to_async
def remove_session(session_key, delete=False):
    session = Session.objects.get(key=session_key)
    session.is_active = False
    session.save()
    if delete:
        session.delete()

    # print("deleting session:", session_key)
    # print("removed session from queue", session_key, session_key not in get_current_queue())
    return '{}'


@database_sync_to_async
def get_place_in_line(session):
    queue = list(
    Session.objects.all().order_by('created_at').filter(is_active=True, in_room=False).values_list('key', flat=True))
    return queue.index(session)

@database_sync_to_async
def remove_next_bot_session():
    queue = list(Session.objects.all().order_by('created_at').filter(is_active=True).values_list('key', flat=True))
    if 'bot_session_' in queue[0]:
        session = Session.objects.get(key=queue[0])
        session.is_active = False
        session.save()
        session.delete()
        return '{}'

    else:
        return

@database_sync_to_async
def update_session_in_room(session_key):
    all_sessions = Session.objects.all()
    for session in all_sessions:
        session.in_room = False
        session.save()
    session = Session.objects.get(key=session_key)
    session.in_room = True
    session.is_active = False
    session.save()
    print('update_session_in_room:::::::session_key:', session_key, 'in room????', session.in_room)

