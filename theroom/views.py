from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from theroom.models import *


def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    room = TheRoom.objects.last()
    # Render that in the index template
    return render(request, "index.html", {
        "rooms": [room],
})

def theroom(request):
    messages = Message.objects.all()
    context = { "messages": messages }
    return render(request, "theroom.html", context)
