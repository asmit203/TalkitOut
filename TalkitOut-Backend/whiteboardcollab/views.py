from django.shortcuts import render


def index(request):
    return render(request, "whiteboardcollab/index.html")

def room(request, room_name):
    return render(request, "whiteboardcollab/room.html", {"room_name": room_name})