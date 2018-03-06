from django.shortcuts import render, redirect
from theroom.models import *

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
        "template_name": "waiting"
    })


def the_website(request):
    if request.method != 'GET':
        return

    session_key = request.GET.get('session_key', False)
    if not session_key:
        return redirect('/')

    session = Session.objects.get(key=session_key)
    # print("views.py the_website", session.key, session.in_room)

    if session.in_room:
        return render(request, "thewebsite.html", {
            "template_name": "thewebsite",
        })
    else:
        return redirect('/goodbye')



def exit(request):
    session_key = request.GET.get('session_key')
    session = Session.objects.get(key=session_key)
    session.is_active = False
    session.save()
    return redirect('/goodbye')


def goodbye(request):
    return render(request, "exit.html", {
        "template_name": "exit",
    })