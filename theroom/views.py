from django.shortcuts import render, redirect
from theroom.models import *
from theroom.utils import get_place_in_line

def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    room = TheRoom.objects.last()
    print("index!!!", request)
    # Render that in the index template
    return render(request, "index.html", {
        # "rooms": [room],
    })


def the_website(request):
    if request.method != 'GET':
        return

    session = Session.objects.get(key=request.GET['session_key'])
    print("views.py the_website", session.key, session.in_room)

    if session.in_room:
        return render(request, "theroom.html", {})
    else:
        return redirect('/')

def getsession(request):
    print("getting session", request)
    return "here is an answer"

def exit(request):
    print('exiting', request.GET)
    return